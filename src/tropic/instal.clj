(ns tropic.instal
  (:require [clojure.string :as str]
            [tropic.gen :refer [make-map]]
            [tropic.parser :refer [parse]]))

(def INACTIVE "inactive")
(def DONE "done")
(def PHASES ["A" "B" "C" "D" "E" "F"])
(def PARAMS ["R" "S" "T" "U" "V" "W" "X" "Y" "Z"])

(defn capitalize-words
  "Capitalize every word in a string"
  [s]
  (->> (str/split (str s) #"\b")
       (map str/capitalize)
       (str/join)))

(defn #^String cap-first [#^String s]
  (if (< (count s) 2)
    (.toUpperCase s)
    (str (.toUpperCase (subs s 0 1))
         (subs s 1))))

(defn #^String decapitalize [#^String s]
  "Decapitalize a String, i.e convert String to string
or STRING to string"
  (if (< (count s) 2)
    (.toLowerCase s)
    (str (.toLowerCase (subs s 0 1))
         (subs s 1))))

(defn event-name
  [words]
  (let [t (str/replace words #"The|the" "")
        s (str/replace t #"'" "")
        c (capitalize-words s)
        i (str/replace c #" " "")
        ename (decapitalize i)]
    ename))

(defn get-by-key [key xs]
  (map #(get % key) (filter #(get % key) xs)))

(defn inst-name
  [iname]
  (str "int" (cap-first (event-name iname))))

(defn event-str
  [event]
  (let [estr (event-name (:verb event))
        letters (take (- (count (vals event)) 1) PARAMS)]
    (str estr "(" (reduce str (interpose ", " letters)) ")")))

(defn sit-str
  [sit]
  (let [when (:when sit)
        ss (:predicate when)
        params [(:subject when) (:object when)]
        norms (:norms sit)]))

(defn make-phases
  [ename len]
  (let [initial (str "phase(" ename ", " INACTIVE ")")
        phaser (fn [ch] (str "phase(" ename ", phase" ch ")"))
        end (str "phase(" ename ", " DONE ")")
        ps (map phaser (take len PHASES))]
    (cons initial (conj (vec ps) end))))

(defn perm [ev]
  (str "perm(" ev ")"))

(defn unify-params [params roles objects]
  (let [m (meta params)
        subject (if (nil? (:subject params)) "" (:subject params))
        object (if (nil? (:object params)) "" (:object params))
        role (event-name subject)
        obj (event-name object)]
        ;; replace with filter
        ;; role (if (some #(= (event-name subject) %) (map event-name roles)) (event-name subject) nil)
        ;; obj (if (some #(= (event-name object) %) (map event-name objects)) (event-name object) nil)]
    ;; [(str "role(X, " role ")") (str "object(Y, " obj ")")]))
    (if (nil? object)
      (if (nil? subject) nil
          [(str "role(X, " role ")")])
      [(str "role(X, " role ")") (str "object(Y, " obj ")")])))

(defn namify [strs]
  (reduce str strs))

(defn generates [trope roles objects]
  (let [header (str "% GENERATES: " (reduce str (:name trope)) " ----------")
        situations (:situations trope)
        wstrs (map #(event-str (:when %)) situations)
        wparams (map #(unify-params (:when %) roles objects) situations)
        gmake (fn [iname evs cnds] (str iname " generates " (reduce str (interpose ", " evs)) " if " (reduce str (interpose ", " cnds)) ";"))
        gen-a (map gmake wstrs (map #(vector (str "int" (cap-first (str %)))) wstrs) wparams)
        ]
    (cons header gen-a)))


(def types
  ["% TYPES ----------"
   "type Agent;"
   "type Role;"
   "type Trope;"
   "type Phase;"
   "type Place;"
   "type Quest;"
   "type Object;\n"])

(def fluents
  ["% FLUENTS ----------"
   "fluent role(Agent, Role);"
   "fluent phase(Trope, Phase);"
   "fluent at(Agent, Place);\n"])


(defn make-unique [stuff]
  (into [] (set (map event-name (remove nil? (flatten (map vals stuff)))))))

(defn prange [start n]
  (->> PARAMS (drop start) (take n)))

(defn get-params [trope]
  (let [evs (:events trope)
        roles (make-unique (map #(select-keys % [:role :role-a :role-b :from :to]) evs))
        objects (into [] (remove #(or (= "Quest" %) (= "quest" %)) (make-unique (map #(select-keys % [:object]) evs))))
        places (make-unique (map #(select-keys % [:place]) evs))
        quests (into [] (filter #(or (= "Quest" %) (= "quest" %)) (make-unique (map #(select-keys % [:object]) evs))))]
    {:roles (map vector roles PARAMS)
     :objects (map vector objects (prange (count roles) (count objects)))
     :places (map vector places (prange (+ (count roles) (count objects)) (count places)))
     :quests (map vector quests (prange (+ (count roles) (count objects) (count places)) (count quests)))}))

(defn external-events [trope]
  (let [header (str "% EXTERNAL EVENTS: " (namify (:name trope)) " ----------")
        events (:events trope)
        situations (:situations trope)
        all (concat events situations)
        strng (fn [x] (str "external event " (event-str x) ";"))]
    (cons header (map strng all))))

(defn inst-events [trope]
  (let [header (str "% INST EVENTS: " (reduce str (:name trope)) " ----------")
        nm (inst-name (:name trope))
        params (get-params trope)
        types (flatten (vector
                        (take (count (:roles params)) (repeat "Agent"))
                        (take (count (:objects params)) (repeat "Object"))
                        (take (count (:places params)) (repeat "Place"))
                        (take (count (:quests params)) (repeat "Quest")))
                     )
        instr (str "inst event " nm "(" (reduce str (interpose ", " types)) ")" ";")]
    (cons header [instr])))

(defn terminates [trope roles objects]
  (let [inst (str (inst-name (:name trope)))]))


(defn get-letter [s params]
  (second (first (filter #(= s (first %)) params))))

(defn param-str [event params]
  (let [format (fn [x y] (str x "(" (reduce str (interpose ", " y)) ")"))
        ;; get roles, objects, places, quests for just this event
        roles (map event-name (vals (select-keys event [:role :role-a :role-b :from :to])))
        objects (map event-name (remove #(or (= "Quest" %) (= "quest" %)) (vals (select-keys event [:object]))))
        places (map event-name (vals (select-keys event [:place])))
        quests (map event-name (filter #(or (= "Quest" %) (= "quest" %)) (vals (select-keys event [:object]))))
        ;; format them into role(X, hero) strings by looking up their letters in params
        rstrs (map #(format "role" %) (map vector (map #(get-letter % params) roles) roles))
        ostrs (map #(format "object" %) (map vector (map #(get-letter % params) objects) objects))
        pstrs (map #(format "place" %) (map vector (map #(get-letter % params) places) places))
        qstrs (map #(format "quest" %) (map vector (map #(get-letter % params) quests) quests))
        ]
    ;; put them in a nice list for processing
    (mapcat flatten [rstrs ostrs pstrs qstrs])
    ))

(defn param-strings [event]
  (let [format (fn [x y] (str x "(" (reduce str (interpose ", " y)) ")"))
        roles (map event-name (vals (select-keys event [:role :role-a :role-b :from :to])))
        objects (map event-name (remove #(or (= "Quest" %) (= "quest" %)) (vals (select-keys event [:object]))))
        places (map event-name (vals (select-keys event [:place])))
        quests (map event-name (filter #(or (= "Quest" %) (= "quest" %)) (vals (select-keys event [:object]))))
        rstrs (map #(format "role" %) (map vector PARAMS roles))
        ostrs (map #(format "object" %) (map vector (prange (count roles) (count objects)) objects))
        pstrs (map #(format "place" %) (map vector (prange (+ (count roles) (count objects)) (count places)) places))
        qstrs (map #(format "quest" %) (map vector (prange (+ (count roles) (count objects) (count places)) (count quests)) quests))
        ]
    (mapcat flatten [rstrs ostrs pstrs qstrs])
    ))

(defn inst-letters [trope]
  (let [params (get-params trope)
        num (reduce + [(count (:roles params))
                       (count (:objects params))
                       (count (:places params))
                       (count (:quests params))])]
    (take num PARAMS)))

(defn initiates [trope]
  (let [params (get-params trope)
        inst (str (inst-name (:name trope)) "(" (reduce str (interpose ", " (inst-letters trope))) ")")
        ename (event-name (:name trope))
        header (str "% INITIATES: " (namify (:name trope)) " ----------")
        term-header (str "% TERMINATES: " (namify (:name trope)) " ----------")
        events (:events trope)
        imake (fn [iname evs cnds] (str iname " initiates " (reduce str (interpose ", " evs)) " if " (reduce str (interpose ", " cnds)) ";"))
        ;; ;; tmake (fn [iname evs cnds] (str iname " terminates " (reduce str (interpose ", " evs)) " if " (reduce str (interpose ", " cnds)) ";"))
        estrs (map event-str events)
        pstrs (map #(param-str % params) events)
        perms (map perm estrs)
        phases (make-phases ename (count events))
        evec (conj (into [] (map vector (rest phases) perms)) [(last phases)])
        cvec (conj (into [] (map conj pstrs phases)) [(last (butlast (rest phases)))])
        init-a (map imake (repeat inst) evec cvec)
        ]
    (concat [header] init-a params (first pstrs))
    ;; events
    ;; estrs
    ;; (reduce str (interpose ", " pstrs))
    ;; params
    ))


#_(defn initiates [trope roles objects]
  (let [inst (str (inst-name (:name trope)))
        ename (event-name (:name trope))
        header (str "% INITIATES: " (namify (:name trope)) " ----------")
        term-header (str "% TERMINATES: " (namify (:name trope)) " ----------")
        events (:events trope)
        situations (:situations trope)
        sitnorms (first (map :norms situations))
        wstrs (map #(event-str (:when %)) situations)
        wpvec (map #(perm (event-str (:permission %))) sitnorms)
        wpparams (filter some? (map #(unify-params (:permission %) roles objects) sitnorms))
        wperms (map perm wstrs)
        estrs (map event-str events)
        perms (map perm estrs)
        wparams (map #(unify-params (:when %) roles objects) situations)
        params (map #(unify-params % roles objects) events)
        phases (make-phases ename (count events))
        mphases (rest phases)
        imake (fn [iname evs cnds] (str iname " initiates " (reduce str (interpose ", " evs)) " if " (reduce str (interpose ", " cnds)) ";"))
        tmake (fn [iname evs cnds] (str iname " terminates " (reduce str (interpose ", " evs)) " if " (reduce str (interpose ", " cnds)) ";"))
        evec (conj (into [] (map vector mphases perms)) [(last phases)])
        tvec (conj (into [] (map vector (butlast mphases) perms)) [(last mphases)])
        cvec (conj (into [] (map conj params phases)) [(last (butlast mphases))])
        svec (map vector wperms)
        init-a (map imake (repeat inst) evec cvec)
        term-a (map tmake (repeat inst) (cons [(first phases)] (conj (into [] (map vector (rest phases) perms)) [(last phases)])) tvec)
        init-b (map imake (repeat inst) svec wparams)
        init-c (map imake (repeat (first (map #(str "int" (cap-first (str %))) wstrs))) (map vector wpvec) wpparams)
        ]
    ;; (imake (first evec) (first cvec))
    ;; (map imake (repeat inst) evec cvec)
    ;; (map imake (repeat inst) svec wparams)
    ;; (map imake (map inst-name wstrs) (map vector wpvec) wpparams)
    (concat [header] init-a init-b init-c [term-header] term-a)
    ;; (concat [header] init-a init-b init-c [term-header] term-a)
    ;; wpvec
    ;; events
    ))

(defn instal [hmap]
  (let [;exts (mapcat external-events (:tropes hmap))
        insts (mapcat inst-events (:tropes hmap))
        inits (mapcat #(initiates %) (:tropes hmap))
        ;; gens (mapcat #(generates % (:roles hmap) (:objects hmap)) (:tropes hmap))]
       ]
    ;; (get-params (first (:tropes hmap))))
    ;; (reduce str (interpose "\n" (concat types fluents exts ["\n"] insts ["\n"] inits ["\n"] gens))))
    (reduce str (interpose "\n" (concat types fluents ["\n"] insts ["\n"] inits))))
  )

(defn instal-gen [text]
  (instal (make-map (parse text) text)))

(defn fix-crs [text]
  (clojure.string/replace text "\r" ""))

(defn instal-file [input output]
  (let [text (slurp input)
        result (instal-gen (fix-crs text))]
    (spit output result)))

