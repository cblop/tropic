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
        rstrs (map #(format "role" %) (map vector (map #(get-letter % (:roles params)) roles) roles))
        ostrs (map #(format "object" %) (map vector (map #(get-letter % (:objects params)) objects) objects))
        pstrs (map #(format "place" %) (map vector (map #(get-letter % (:places params)) places) places))
        qstrs (map #(format "quest" %) (map vector (map #(get-letter % (:quests params)) quests) quests))
        ]
    ;; put them in a nice list for processing
    (mapcat flatten [rstrs ostrs pstrs qstrs])
    ))


(defn event-str
  [event params]
  (let [format (fn [xs]  (str (:verb event) "(" (reduce str (interpose ", " xs)) ")"))
        roles (map event-name (vals (select-keys event [:role :role-a :role-b :from :to])))
        objects (map event-name (remove #(or (= "Quest" %) (= "quest" %)) (vals (select-keys event [:object]))))
        places (map event-name (vals (select-keys event [:place])))
        quests (map event-name (filter #(or (= "Quest" %) (= "quest" %)) (vals (select-keys event [:object]))))
        rletters (sort (map #(get-letter % (:roles params)) roles))
        oletters (sort (map #(get-letter % (:objects params)) objects))
        pletters (sort (map #(get-letter % (:places params)) places))
        qletters (sort (map #(get-letter % (:quests params)) quests))
        ]
    (format (flatten [rletters oletters pletters qletters]))
    ))

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

(defn ev-types [event]
  (let [roles (map event-name (vals (select-keys event [:role :role-a :role-b :from :to])))
        objects (map event-name (remove #(or (= "Quest" %) (= "quest" %)) (vals (select-keys event [:object]))))
        places (map event-name (vals (select-keys event [:place])))
        quests (map event-name (filter #(or (= "Quest" %) (= "quest" %)) (vals (select-keys event [:object]))))
        types (flatten (vector
                        (take (count roles) (repeat "Agent"))
                        (take (count objects) (repeat "ObjectName"))
                        (take (count places) (repeat "PlaceName"))
                        (take (count quests) (repeat "Quest")))
                       )]
    types
    ))

(defn obl-p [{:keys [obligation]} params]
  (let [deadline (:deadline obligation)
        violation (:violation obligation)
        obl (if (nil? obligation) ""
                (->> obligation
                    (ev-types)
                    (interpose ", ")
                    (reduce str)
                    ;; (reduce str (param-str params))
                    ))
        dead (if (nil? deadline) "noDeadline"
                 (->> deadline
                     (ev-types)
                     (interpose ", ")
                     (reduce str)
                     ;; (reduce str (param-str params))
                     ))
        viol (if (nil? violation) "noViolation"
                 (->> violation
                     (ev-types)
                     (interpose ", ")
                     (reduce str)
                     ;; (reduce str)(param-str params)
                     ))]
    (str "obl(" (:verb obligation) "(" obl "), " (:verb deadline) "(" dead ")" ", " viol ");")))

(defn obl [{:keys [obligation]} params]
  (let [deadline (:deadline obligation)
        violation (:violation obligation)
        p (println "OBLS: ")
        x (println params)
        d (println "DEAD: ")
        y (println (event-str deadline params))
        obl (if (nil? obligation) ""
                (-> obligation
                    (event-str params)
                    ;; (param-str params)
                    ))
        dead (if (nil? deadline) "noDeadline"
                 (event-str deadline params))
        viol (if (nil? violation) "noViolation"
                 (-> violation
                     (event-str params)
                     ;; (param-str params)
                     ))
        s (println "WHAT: ")
        t (println (str "obl(" obl ", " dead ", " viol ")"))
        ]
            (str "obl(" obl ", " dead ", " viol ")")))

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

(def types
  ["% TYPES ----------"
   "type Agent;"
   "type Role;"
   "type Trope;"
   "type Phase;"
   "type Place;"
   "type PlaceName;"
   "type Quest;"
   "type Object;"
   "type ObjectName;\n"])

(def fluents
  ["% FLUENTS ----------"
   "fluent role(Agent, Role);"
   "fluent phase(Trope, Phase);"
   "fluent place(PlaceName, Place);"
   "fluent object(ObjectName, Object);"
   "fluent at(Agent, Place);\n"])


(defn make-unique [stuff]
  (into [] (set (map event-name (remove nil? (flatten (map vals stuff)))))))

(defn prange [start n]
  (->> PARAMS (drop start) (take n)))

(defn get-params [trope]
  (let [events (remove :obligation (:events trope))
        ;; might need to select-keys :obl :dead :viol
        obls (map :obligation (filter :obligation (:events trope)))
        evs (concat events obls)
        roles (make-unique (map #(select-keys % [:role :role-a :role-b :from :to]) evs))
        objects (into [] (remove #(or (= "Quest" %) (= "quest" %)) (make-unique (map #(select-keys % [:object]) evs))))
        places (make-unique (map #(select-keys % [:place]) evs))
        quests (into [] (filter #(or (= "Quest" %) (= "quest" %)) (make-unique (map #(select-keys % [:object]) evs))))]
    {:roles (map vector roles PARAMS)
     :objects (map vector objects (prange (count roles) (count objects)))
     :places (map vector places (prange (+ (count roles) (count objects)) (count places)))
     :quests (map vector quests (prange (+ (count roles) (count objects) (count places)) (count quests)))}))

(defn get-all-params [trope]
  (let [
        sits (map :when (filter :when (:situations trope)))
        perms (flatten (map #(map :permission (filter :permission %)) (map :norms (:situations trope))))
        obls (map :obligation (filter :obligation (:events trope)))
        deads (map :deadline (map :obligation (filter :obligation (:events trope))))
        ;; wpvec (map (fn [x] (map #(perm (event-str (:permission %) sparams)) (filter :permission x))) sitnorms)
        evs (concat sits perms obls deads (:events trope))
        roles (make-unique (map #(select-keys % [:role :role-a :role-b :from :to]) evs))
        objects (into [] (remove #(or (= "Quest" %) (= "quest" %)) (make-unique (map #(select-keys % [:object]) evs))))
        places (make-unique (map #(select-keys % [:place]) evs))
        quests (into [] (filter #(or (= "Quest" %) (= "quest" %)) (make-unique (map #(select-keys % [:object]) evs))))]
    {:roles (map vector roles PARAMS)
     :objects (map vector objects (prange (count roles) (count objects)))
     :places (map vector places (prange (+ (count roles) (count objects)) (count places)))
     :quests (map vector quests (prange (+ (count roles) (count objects) (count places)) (count quests)))}))

(defn get-obl-params [trope]
  (let [
        obls (map :obligation (filter :obligation (:events trope)))
        deads (map :deadline (filter :deadline obls))
        viols (map :violation (filter :violation obls))
        os (map #(-> % (dissoc :deadline) (dissoc :violation)) obls)
        ;; o (println "deads: ")
        ;; p (println obls)
        ;; wpvec (map (fn [x] (map #(perm (event-str (:permission %) sparams)) (filter :permission x))) sitnorms)
        evs (concat os deads viols)
        roles (make-unique (map #(select-keys % [:role :role-a :role-b :from :to]) evs))
        objects (into [] (remove #(or (= "Quest" %) (= "quest" %)) (make-unique (map #(select-keys % [:object]) evs))))
        places (make-unique (map #(select-keys % [:place]) evs))
        quests (into [] (filter #(or (= "Quest" %) (= "quest" %)) (make-unique (map #(select-keys % [:object]) evs))))]
    {:roles (map vector roles PARAMS)
     :objects (map vector objects (prange (count roles) (count objects)))
     :places (map vector places (prange (+ (count roles) (count objects)) (count places)))
     :quests (map vector quests (prange (+ (count roles) (count objects) (count places)) (count quests)))}))

(defn get-dead-params [sit]
  (let [
        sits (:deadline sit)
        ;; wpvec (map (fn [x] (map #(perm (event-str (:permission %) sparams)) (filter :permission x))) sitnorms)
        evs [sits]
        roles (make-unique (map #(select-keys % [:role :role-a :role-b :from :to]) evs))
        objects (into [] (remove #(or (= "Quest" %) (= "quest" %)) (make-unique (map #(select-keys % [:object]) evs))))
        places (make-unique (map #(select-keys % [:place]) evs))
        quests (into [] (filter #(or (= "Quest" %) (= "quest" %)) (make-unique (map #(select-keys % [:object]) evs))))]
    {:roles (map vector roles PARAMS)
     :objects (map vector objects (prange (count roles) (count objects)))
     :places (map vector places (prange (+ (count roles) (count objects)) (count places)))
     :quests (map vector quests (prange (+ (count roles) (count objects) (count places)) (count quests)))}))

(defn get-when-params [sit]
  (let [
        sits (:when sit)
        ;; wpvec (map (fn [x] (map #(perm (event-str (:permission %) sparams)) (filter :permission x))) sitnorms)
        evs [sits]
        roles (make-unique (map #(select-keys % [:role :role-a :role-b :from :to]) evs))
        objects (into [] (remove #(or (= "Quest" %) (= "quest" %)) (make-unique (map #(select-keys % [:object]) evs))))
        places (make-unique (map #(select-keys % [:place]) evs))
        quests (into [] (filter #(or (= "Quest" %) (= "quest" %)) (make-unique (map #(select-keys % [:object]) evs))))]
    {:roles (map vector roles PARAMS)
     :objects (map vector objects (prange (count roles) (count objects)))
     :places (map vector places (prange (+ (count roles) (count objects)) (count places)))
     :quests (map vector quests (prange (+ (count roles) (count objects) (count places)) (count quests)))}))

(defn get-sit-params [trope]
  (let [
        sits (map :when (filter :when (:situations trope)))
        perms (flatten (map #(map :permission (filter :permission %)) (map :norms (:situations trope))))
        ;; wpvec (map (fn [x] (map #(perm (event-str (:permission %) sparams)) (filter :permission x))) sitnorms)
        evs (concat sits perms)
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
        params (get-params trope)
        evs (remove :obligation (:events trope))
        deads (remove nil? (map #(-> % :obligation :deadline) (:events trope)))
        p (println (:events trope))
        events (concat evs deads)
        situations (map :when (:situations trope))
        sperms (mapcat #(map :permission (filter :permission %)) (map :norms (:situations trope)))
        all (concat events situations sperms)
        types (map ev-types all)
        strng (fn [x y] (str "exogenous event " (event-name (:verb x)) "(" (reduce str (interpose ", " y)) ")" ";"))]
    (concat (cons header (into [] (set (map (fn [x y] (strng x y)) all types)))) ["exogenous event noDeadline;"])))
    ;; (prn-str types)
  ;; ))

(defn viol-events [trope]
  (let [header (str "% VIOLATION EVENTS: " (namify (:name trope)) " ----------")
        ;; params (get-obl-params trope)
        viols (map #(-> % :obligation :violation) (:events trope))
        types (map ev-types (:permission viols))
        ;; types []
        ;; all []
        strng (fn [x y] (str "violation event " (event-name (:verb x)) "(" (reduce str (interpose ", " y)) ")" ";"))]
    (concat (cons header (into [] (set (map (fn [x y] (strng x y)) viols types)))) ["violation event noViolation;"])))

(defn get-param-obls [trope]
  (let [
        obls (map :obligation (filter :obligation (:events trope)))
        deads (map :deadline (filter :deadline obls))
        ;; deads (if (empty? ds) [{:verb "noDeadline"}] ds)
        viols (map :violation (filter :violation obls))
        ;; viols (if (empty? vs) [{:verb "noViolation"}] vs)
        os (map #(-> % (dissoc :deadline) (dissoc :violation)) obls)
        oevs (concat os deads viols)
        oparams (get-obl-params trope)
        ;; wpvec (map (fn [x] (map #(perm (event-str (:permission %) sparams)) (filter :permission x))) sitnorms)
        ;; pobls (map #(perm (event-str % oparams)) os)
        ;; pdeads (map #(perm (event-str % oparams)) deads)
        ;; ostrs (into [] (set (map #(event-str % oparams) oevs)))
        stypes (fn [x] (flatten (vector
                                 (take (count (:roles x)) (repeat "Agent"))
                                 (take (count (:objects x)) (repeat "ObjectName"))
                                 (take (count (:places x)) (repeat "PlaceName"))
                                 (take (count (:quests x)) (repeat "Quest"))
                                 )))
        ot (map stypes oparams)
        pobls (map #(obl-p % oparams) (filter :obligation (:events trope)))
        ostrs (map #(str (inst-name (:verb %)) "(" (reduce str (interpose ", " ot)) ")") deads)
        oifs (mapcat #(param-str % oparams) oevs)
        o (println "oifs: ")
        p (println oifs)
        ]
    {:names ostrs :evs [pobls] :deads deads :viols viols :conds [oifs]}))

(defn in? 
  "true if seq contains elm"
  [seq elm]
  (some #(= elm %) seq))

(defn lookup-obl-letters [trope obl]
  (let [params (get-obl-params trope)
        vs (map event-name (vals (dissoc obl :verb)))
        ps (apply concat (vals params))
        ls (map second (filter #(in? vs (first %)) ps))]
    ls))


(defn get-obls [trope]
  (let [
        obls (map :obligation (filter :obligation (:events trope)))
        deads (map :deadline (filter :deadline obls))
        ;; deads (if (empty? ds) [{:verb "noDeadline"}] ds)
        viols (map :violation (filter :violation obls))
        ;; viols (if (empty? vs) [{:verb "noViolation"}] vs)
        os (map #(-> % (dissoc :deadline) (dissoc :violation)) obls)
        oevs (concat os deads viols)
        oparams (get-obl-params trope)
        ;; wpvec (map (fn [x] (map #(perm (event-str (:permission %) sparams)) (filter :permission x))) sitnorms)
        pobls (map #(obl % oparams) (filter :obligation (:events trope)))
        ;; pobls (map #(perm (event-str % oparams)) os)
        ;; pdeads (map #(perm (event-str % oparams)) deads)
        ;; ostrs (into [] (set (map #(event-str % oparams) oevs)))
        ostrs (map #(str (inst-name (:verb %)) "(" (reduce str (interpose ", " (lookup-obl-letters trope %))) ")") deads)
        oifs (mapcat #(param-str % oparams) oevs)
        o (println "oifs: ")
        p (println oifs)
        ]
    {:names ostrs :evs [pobls] :deads deads :viols viols :conds [oifs]}))

(defn obl-events [trope]
  (let [header (str "% OBLIGATION FLUENTS: " (namify (:name trope)) " ----------")
        obls (get-param-obls trope)
        strng (fn [x] (str "obligation fluent " (reduce str x)))]
        (cons header (into [] (map strng (:evs obls))))))


(defn inst-events [trope]
  (let [header (str "% INST EVENTS: " (reduce str (:name trope)) " ----------")
        nm (inst-name (:name trope))
        snms (map inst-name (map :verb (map :when (:situations trope))))
        onms (map inst-name (map :verb (map :obligation (filter :obligation (:events trope)))))
        params (get-all-params trope)
        sparams (map get-when-params (:situations trope))
        oparams (map get-dead-params (map :obligation (filter :obligation (:events trope))))
        types (flatten (vector
                        (take (count (:roles params)) (repeat "Agent"))
                        (take (count (:objects params)) (repeat "ObjectName"))
                        (take (count (:places params)) (repeat "PlaceName"))
                        (take (count (:quests params)) (repeat "Quest")))
                     )
        stypes (fn [x] (flatten (vector
                                 (take (count (:roles x)) (repeat "Agent"))
                                 (take (count (:objects x)) (repeat "ObjectName"))
                                 (take (count (:places x)) (repeat "PlaceName"))
                                 (take (count (:quests x)) (repeat "Quest"))
                                 )))
        ss (map stypes sparams)
        os (map stypes oparams)
        o (println "os: ")
        p (println oparams)
        finstr (fn [x ys] (str "inst event " x "(" (reduce str (interpose ", " ys)) ")" ";"))
        instr (str "inst event " nm "(" (reduce str (interpose ", " types)) ")" ";")
        sinstrs (map finstr snms ss)
        oinstrs (map (fn [xs ys] (if (empty? ys) "" (finstr xs ys))) onms os)
        ]
    (cons header (conj (concat sinstrs oinstrs) instr))))

(defn terminates [trope roles objects]
  (let [inst (str (inst-name (:name trope)))]))

(defn param-str [event params]
  (let [format (fn [x y] (str x "(" (reduce str (interpose ", " y)) ")"))
        ;; get roles, objects, places, quests for just this event
        roles (map event-name (vals (select-keys event [:role :role-a :role-b :from :to])))
        objects (map event-name (remove #(or (= "Quest" %) (= "quest" %)) (vals (select-keys event [:object]))))
        places (map event-name (vals (select-keys event [:place])))
        quests (map event-name (filter #(or (= "Quest" %) (= "quest" %)) (vals (select-keys event [:object]))))
        ;; format them into role(X, hero) strings by looking up their letters in params
        rstrs (map #(format "role" %) (map vector (map #(get-letter % (:roles params)) roles) roles))
        ostrs (map #(format "object" %) (map vector (map #(get-letter % (:objects params)) objects) objects))
        pstrs (map #(format "place" %) (map vector (map #(get-letter % (:places params)) places) places))
        qstrs (map #(format "quest" %) (map vector (map #(get-letter % (:quests params)) quests) quests))
        ]
    ;; put them in a nice list for processing
    (mapcat flatten [rstrs ostrs pstrs qstrs])
    ))


(defn inst-letters [trope]
  (let [params (get-all-params trope)
        num (reduce + [(count (:roles params))
                       (count (:objects params))
                       (count (:places params))
                       (count (:quests params))])]
    (take num PARAMS)))


(defn lookup-sit-letters [trope sit]
  (let [params (get-sit-params trope)
        vs (map event-name (vals (dissoc (:when sit) :verb)))
        ps (apply concat (vals params))
        ls (map second (filter #(in? vs (first %)) ps))]
    ls))

(defn sit-letters [sit]
  (let [num (count (remove :verb sit))]
    (take num PARAMS)))

(defn obl-letters [obl]
  (let [num (count (dissoc obl :verb))]
    (take num PARAMS)))


(defn generates [trope]
  (let [params (get-all-params trope)
        oparams (get-obl-params trope)
        obls (map :obligation (filter :obligation (:events trope)))
        deads (map :deadline (filter :deadline obls))
        viols (map :violation (filter :violation obls))
        os (map #(-> % (dissoc :deadline) (dissoc :violation)) obls)
        oevs (concat os deads viols)
        wparams (flatten (map get-when-params (:situations trope)))
        ;; wparams (get-params trope)
        header (str "% GENERATES: " (reduce str (:name trope)) " ----------")
        inst (str (inst-name (:name trope)) "(" (reduce str (interpose ", " (inst-letters trope))) ")")
        situations (:situations trope)
        o (println "GENS: ")
        p (println params)
        ;; q (println oevs)
        ;; sit-conds (map :when (filter :when situations))
        wnames (map #(str (inst-name (:verb (:when %))) "(" (reduce str (interpose ", " (sit-letters %))) ")") situations)
        onames (map #(str (inst-name (:verb %)) "(" (reduce str (interpose ", " (lookup-obl-letters trope %))) ")") oevs)
        ename (event-name (:name trope))
        events (remove :obligation (:events trope))
        wstrs (map (fn [x ys] (event-str (:when x) ys)) situations wparams)
        ostrs (into [] (set (map #(event-str % oparams) oevs)))
        ;; wparams (map #(unify-params (:when %) roles objects) situations)
        gmake (fn [iname ev cnds] (str ev " generates " iname " if " (reduce str (interpose ", " cnds)) ";"))
        estrs (map #(event-str % params) events)
        pstrs (map #(param-str % params) events)
        wifs (map (fn [x ys] (param-str x ys)) (map :when (filter :when situations)) wparams)
        ;; oifs (map (fn [x ys] (param-str x ys)) oevs oparams)
        oifs (map #(param-str % oparams) oevs)
        ;; perms (map perm estrs)
        ;; phases (make-phases ename (count events))
        ;; evec (conj (into [] (map vector (rest phases) perms)) [(last phases)])
        ;; cvec (conj (into [] (map conj pstrs phases)) [(last (butlast (rest phases)))])
        gen-a (into [] (set (map gmake (repeat inst) estrs pstrs)))
        gen-s (map gmake wnames wstrs wifs)
        gen-d (map (fn [w x y z] (if (empty? w) "" (gmake x y z))) deads onames ostrs oifs)
        ]
    (concat [header] gen-a gen-s gen-d)
    ))


(defn merge-lists [& maps]
  (reduce (fn [m1 m2]
            (reduce (fn [m [k v]]
                      (update-in m [k] (fnil concat []) v))
                    m1, m2))
          {}
          maps))


(defn initially [hmap]
  (let [
        header "\n% INITIALLY: -----------"
        params (apply merge (map get-all-params (:tropes hmap)))
        ;; qq (println "all-params: ")
        ;; q (println params)
        obls (map get-obls (:tropes hmap))
        story (:story hmap)
        instances (:instances story)
        role-list (map first (:roles params))
        place-list (map first (:places params))
        obj-list (map first (:objects params))
        ;event-name?
        roles (filter #(in? role-list (event-name (:class %))) instances)
        places (filter #(in? place-list (event-name (:class %))) instances)
        objects (filter #(in? obj-list (event-name (:class %))) instances)
        fluentfn (fn [x t] (str t "(" (event-name (:iname x)) ", " (event-name (:class x)) ")"))
        rolestrs (map #(fluentfn % "role") roles)
        placestrs (map #(fluentfn % "place") places)
        objstrs (map #(fluentfn % "object") objects)
        phasefn (fn [x] (str "phase(" x ", " INACTIVE ")"))
        phases (map #(event-name (:name %)) (:tropes hmap))
        phasestrs (map phasefn phases)
        powfn (fn [x] (let [letters (inst-letters x)
                            cnds (reduce str (flatten (interpose ", " (map #(interpose "!=" %) (partition 2 letters)))))]
                        (str "pow(" (inst-name (:name x))
                             "(" (reduce str (interpose ", " letters))
                             ;; ")) if " cnds)))
                             "))")))
        situations (mapcat :situations (:tropes hmap))
        wpnames (map #(str "pow(" (inst-name (:verb (:when %))) "(" (reduce str (interpose ", " (sit-letters %))) "))") situations)
        opnames (map #(str "pow(" % ")") (mapcat :names obls))
        o (println "opnames: ")
        p (println opnames)
        powers (map powfn (:tropes hmap))]
    ;; (concat rolestrs placestrs)
    ;; (concat role-list place-list)
    ;; roles
    ;; (map #(event-name (:class %)) instances)
    [header (str "initially\n    " (reduce str (interpose ",\n    " (concat powers wpnames opnames phasestrs rolestrs placestrs objstrs))) ";\n")]
    ;; (map :class instances)
    ))

(defn get-sits [trope]
  (let [situations (:situations trope)
        sitnorms (map :norms situations)
        sitevs (flatten (map #(map :permission (filter :permission %)) sitnorms))
        sparams (get-sit-params trope)
        wstrs (map #(str (inst-name (:verb (:when %))) "(" (reduce str (interpose ", " (lookup-sit-letters trope %))) ")") situations)
        wpvec (map (fn [x] (map #(perm (event-str (:permission %) sparams)) (filter :permission x))) sitnorms)
        wpparams (map #(param-str % sparams) sitevs)
        ]
    {:names wstrs :events wpvec :conds wpparams}))

(defn norm-str [event params]
  (if (:obligation event) (obl event params)
    (perm (event-str event params))))

(defn norm-params [ev params]
  (if (:obligation ev)  (mapcat #(param-str % params) [(:obligation ev) (:deadline (:obligation ev)) (:violation (:obligation ev))])
    (param-str ev params)))

(defn initiates [trope]
  (let [params (get-all-params trope)
        p (println "PARAMS: ")
        q (println params)
        inst (str (inst-name (:name trope)) "(" (reduce str (interpose ", " (inst-letters trope))) ")")
        ename (event-name (:name trope))
        header (str "% INITIATES: " (namify (:name trope)) " ----------")
        term-header (str "% TERMINATES: " (namify (:name trope)) " ----------")
        ;; events (remove :obligation (:events trope))
        events (:events trope)
        imake (fn [iname evs cnds] (str iname " initiates " (reduce str (interpose ", " evs)) " if " (reduce str (interpose ", " cnds)) ";"))
        tmake (fn [iname evs cnds] (str iname " terminates " (reduce str (interpose ", " evs)) " if " (reduce str (interpose ", " cnds)) ";"))
        ;; estrs (map #(event-str % params) events)
        estrs (map #(norm-str % params) events)
        pstrs (map #(norm-params % params) events)
        ;; perms (map perm estrs)
        ;; oblis (map #(obl % params) (filter :obligation (:events trope)))
        ;; norms (concat perms oblis)
        norms estrs
        ;; norms perms
        phases (make-phases ename (count events))
        evec (conj (into [] (map vector (rest phases) norms)) [(last phases)])
        cvec (conj (into [] (map conj pstrs phases)) [(last (butlast (rest phases)))])
        sits (get-sits trope)
        obls (get-obls trope)
        ;; tvec (conj phases [(last phases)])
        tvec (map vector phases)
        init-a (map imake (repeat inst) evec cvec)
        init-s (map imake (:names sits) (:events sits) (:conds sits))
        term-o (map tmake (:names obls) (:evs obls) (:conds obls))
        term-a (map tmake (repeat inst) (cons [(first phases)] (conj (into [] (map vector (rest phases) norms)) [(last phases)])) tvec)
        ]
    (concat [header] init-a init-s [term-header] term-a term-o)
    ))


(defn instal [hmap]
  (let [;; initiallys [(str "initially\n    " (reduce str (interpose ",\n    " (mapcat #(initially % story) (:tropes hmap)))) ";")]
        initiallys (initially hmap)
        inst-name [(str "institution " (event-name (:storyname (:story hmap))) ";")]
        create ["% CREATION EVENT -----------" "create event startShow;\n"]
        exts (mapcat external-events (:tropes hmap))
        insts (mapcat inst-events (:tropes hmap))
        obls (mapcat obl-events (:tropes hmap))
        inits (mapcat #(initiates %) (:tropes hmap))
        gens (mapcat generates (:tropes hmap))
        viols (mapcat viol-events (:tropes hmap))
       ]
    ;; (get-params (first (:tropes hmap))))
    ;; (reduce str (interpose "\n" (concat types fluents exts ["\n"] insts ["\n"] inits ["\n"] gens))))
    (reduce str (interpose "\n" (concat inst-name types fluents exts viols insts obls inits gens initiallys))))
  )

(defn instal-gen [text]
  (instal (make-map (parse text) text)))

(defn fix-crs [text]
  (clojure.string/replace text "\r" ""))

(defn instal-file [input output]
  (let [text (slurp input)
        result (instal-gen (fix-crs text))]
    (spit output result)))

