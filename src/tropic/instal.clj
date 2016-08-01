(ns tropic.instal
  (:require [clojure.string :as str]))

(def INACTIVE "inactive")
(def DONE "done")
(def PHASES ["A" "B" "C" "D" "E" "F"])
(def PARAMS ["R" "S" "T" "U" "V" "W" "X" "Y" "Z"])
(def WS "    ")

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

(defn inst-start-name
  [iname]
  (str "intStart" (cap-first (event-name iname))))

(defn inst-stop-name
  [iname]
  (str "intStop" (cap-first (event-name iname))))

(defn get-letter [s params]
  (second (first (filter #(= s (first %)) params))))


(defn param-str [ev params]
  (let [event (or (:permission ev) (:obligation ev) ev)
        format (fn [x y] (str x "(" (reduce str (interpose ", " y)) ")"))
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

(defn param-brackets
  [event params]
  (let [format (fn [xs]  (str "(" (reduce str (interpose ", " xs)) ")"))
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

(defn event-str
  [event params]
  (let [format (fn [xs]  (str (if (:verb event) (event-name (:verb event)) "") "(" (reduce str (interpose ", " xs)) ")"))
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
                        ;; (take (count quests) (repeat "Quest"))
                        )
                       )]
    types
    ))


(defn viol-name [obl]
  (let [vstuff (-> obl
                   (:obligation)
                   (dissoc :deadline)
                   (dissoc :violation)
                   (vals)
                   )
        name (cap-first (event-name (reduce str (interpose " " vstuff))))]
    (str "viol" (reduce str name))))

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
        dead (if (nil? deadline) "noDeadline(Identity)"
                 (str (:verb deadline) "(" (->> deadline
                                                (ev-types)
                                                (interpose ", ")
                                                (reduce str)
                                                ;; (reduce str (param-str params))
                                                ) ")"))
        viol (if (nil? violation) "noViolation(Identity)"
                 (viol-name {:obligation obligation}))]
    (str "obl(" (:verb obligation) "(" obl "), " dead ", " viol ");")))

(defn obl [{:keys [obligation]} params]
  (let [deadline (:deadline obligation)
        violation (:violation obligation)
        obl (if (nil? obligation) ""
                (-> obligation
                    (event-str params)
                    ;; (param-str params)
                    ))
        dead (if (nil? deadline) "noDeadline(Identity)"
                 (event-str deadline params))
        viol (if (nil? violation) "noViolation(Identity)"
                 (viol-name {:obligation obligation})
                     ;; (param-str params)
                     )
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
   "type Identity;"
   "type Agent;"
   "type Role;"
   "type Trope;"
   "type Phase;"
   "type Place;"
   "type PlaceName;"
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
        eperms (map :permission (filter :permission (:events trope)))
        aperms (concat perms eperms)
        obls (map :obligation (filter :obligation (:events trope)))
        deads (map :deadline (map :obligation (filter :obligation (:events trope))))
        ;; wpvec (map (fn [x] (map #(perm (event-str (:permission %) sparams)) (filter :permission x))) sitnorms)
        evs (concat sits aperms obls deads (:events trope))
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
  (let [header (str "% EXTERNAL EVENTS: " (namify (:label trope)) " ----------")
        params (get-params trope)
        es (remove :obligation (:events trope))
        evs (map #(or (:permission %) %) es)
        deads (remove nil? (map #(-> % :obligation :deadline) (:events trope)))
        obls (remove nil? (map :obligation (:events trope)))
        events (concat evs obls deads)
        situations (map :when (:situations trope))
        sperms (mapcat #(map :permission (filter :permission %)) (map :norms (:situations trope)))
        all (concat events situations sperms)
        types (map ev-types all)
        strng (fn [x y] (if (:verb x) (str "exogenous event " (event-name (:verb x)) "(" (reduce str (interpose ", " y)) ")" ";")))]
    (concat (cons header (into [] (set (map (fn [x y] (strng x y)) all types)))) ["exogenous event noDeadline(Identity);"])))
    ;; (prn-str types)
  ;; ))


(defn viol-events [trope]
  (let [header (str "\n% VIOLATION EVENTS: " (namify (:label trope)) " ----------")
        viols (filter :obligation (:events trope))
        strng (fn [x] (str "violation event " (viol-name x)";"))]
    (concat (cons header (into [] (set (map strng viols)))) ["violation event noViolation(Identity);"])))

(defn get-param-obls [trope]
  (let [
        obls (map :obligation (filter :obligation (:events trope)))
        deads (map :deadline (filter :deadline obls))
        ;; deads (if (empty? ds) [{:verb "noDeadline"}] ds)
        ;; viols (map :violation (filter :violation obls))
        vs (map :violation (filter :violation obls))
        viols (if (empty? vs) [{:verb "noViolation"}] vs)
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
        ]
    {:names ostrs :evs (into [] pobls) :deads deads :viols viols :conds [oifs]}))

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
        ]
    {:names ostrs :evs (into [] pobls) :deads deads :viols viols :conds [oifs]}))

(defn obl-events [trope]
  (let [header (str "\n% OBLIGATION FLUENTS: " (namify (:label trope)) " ----------")
        obls (get-param-obls trope)
        strng (fn [x] (str "obligation fluent " (reduce str x)))]
    (if-not (empty? (reduce str (:evs obls)))
      (cons header (into [] (map strng (:evs obls))))
      "\n"
      )))

;; cross fluent ipow(Inst, perm(go(X, Y)), Inst)
;; initially ipow(herosJourney, perm(go(X, Y)), quest)

(defn get-subtropes [trope tropes]
  (let [stropes (map #(if-let [s (:subtrope %)]
                        (first (filter (fn [x] (or (= (:label x) (str "The " s)) (= (:label x) s))) tropes))
                        nil) (:events trope))]
    (remove nil? stropes)))


(defn get-blocked-tropes [trope tropes]
  (let [stropes (map #(if-let [s (:block %)]
                        (first (filter (fn [x] (or (= (:label x) (str "The " s)) (= (:label x) s))) tropes))
                        nil) (:events trope))]
    (remove nil? stropes)))

(defn inst-events [trope tropes]
  (let [header (str "\n% INST EVENTS: " (reduce str (:label trope)) " ----------")
        nm (inst-name (:label trope))
        snms (map inst-name (map :verb (map :when (:situations trope))))
        ;; dnms (map inst-name (map #(:verb (:deadline (:obligation %))) (filter :obligation (:events trope))))
        dnms (map inst-name (remove nil? (map #(:verb (:deadline (:obligation %))) (filter :obligation (:events trope)))))
        obnms (map inst-name (map :verb (map :obligation (filter :obligation (:events trope)))))
        onms (concat dnms obnms)
        params (get-all-params trope)
        sparams (map get-when-params (:situations trope))
        oparams (map get-dead-params (map :obligation (filter :obligation (:events trope))))
        subs (get-subtropes trope tropes)
        subparams (map get-all-params (map #(assoc % :events [(first (:events %))]) subs))
        ;; subparams (map get-all-params subs)
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
        subss (map stypes subparams)
        finstr (fn [x ys] (str "inst event " x "(" (reduce str (interpose ", " ys)) ")" ";"))
        instr (str "inst event " nm "(" (reduce str (interpose ", " types)) ")" ";")
        sinstrs (map finstr snms ss)
        oinstrs (map (fn [xs ys] (if (empty? ys) "" (finstr xs ys))) onms os)
        subinstrs (map #(finstr (inst-start-name (:label %1)) %2) subs subss)
        ]
    (cons header (conj (concat sinstrs oinstrs subinstrs) instr))))

(defn terminates [trope roles objects]
  (let [inst (str (inst-name (:label trope)))]))

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

(defn subs-triggers [trope tropes]
  (map-indexed (fn [i e]
                 (if-let [sub (:subtrope e)]
                   (let [subtrope (first (filter #(= (:label %) (or (str "The " sub) sub)) tropes))]
                     (if (> i 0)
                       {:subtrope subtrope
                        :phase (nth PHASES (dec i))
                        :trigger (nth (:events trope) (dec i))}
                       {:subtrope subtrope})))) (:events trope)))

(defn generates [trope tropes]
  (let [params (get-all-params trope)
        oparams (get-obl-params trope)
        obls (map :obligation (filter :obligation (:events trope)))
        deads (map :deadline (filter :deadline obls))
        viols (map :violation (filter :violation obls))
        os (map #(-> % (dissoc :deadline) (dissoc :violation)) obls)
        oevs (concat os deads viols)
        wparams (flatten (map get-when-params (:situations trope)))
        subs (subs-triggers trope tropes)
        header (str "% GENERATES: " (reduce str (:label trope)) " ----------")
        inst (str (inst-name (:label trope)) "(" (reduce str (interpose ", " (inst-letters trope))) ")")
        situations (:situations trope)
        wnames (map #(str (inst-name (:verb (:when %))) "(" (reduce str (interpose ", " (sit-letters %))) ")") situations)
        onames (map #(str (inst-name (:verb %)) "(" (reduce str (interpose ", " (lookup-obl-letters trope %))) ")") oevs)
        ename (event-name (:label trope))
        events (remove :obligation (:events trope))
        wstrs (map (fn [x ys] (event-str (:when x) ys)) situations wparams)
        ostrs (into [] (set (map #(event-str % oparams) oevs)))
        gmake (fn [iname ev cnds] (if-not (= "()" ev) (str ev " generates\n" WS iname " if\n" WS WS (reduce str (interpose (str ",\n" WS WS) cnds)) ";")))
        estrs (map #(event-str % params) events)
        pstrs (map #(param-str % params) events)
        wifs (map (fn [x ys] (param-str x ys)) (map :when (filter :when situations)) wparams)
        oifs (map #(param-str % oparams) oevs)
        smake (fn [sub]
                (if (:subtrope sub)
                  (let [pms (get-all-params (assoc trope :events (concat (:events trope) (:events (:subtrope sub)))))
                        int (event-name (:label trope))
                        ]
                    (gmake (str (inst-start-name (:label (:subtrope sub))) (param-brackets (first (:events (:subtrope sub))) pms)) (event-str (:trigger sub) pms) (concat (param-str (first (:events (:subtrope sub))) pms) (param-str (:trigger sub) pms) [(str "phase(" int ", " "phase" (:phase sub) ")")])))))
        gen-subs (remove nil? (map smake subs))
        gen-a (into [] (set (map gmake (repeat inst) estrs pstrs)))
        gen-s (map gmake wnames wstrs wifs)
        gen-d (map (fn [w x y z] (if (empty? w) "" (gmake x y z))) deads onames ostrs oifs)
        ]
    (concat [header] gen-subs gen-a gen-s gen-d ["\n"])
    ))


(defn bridge [tropes]
  (let [;; ievents (subs-triggers tropes)
        subtropes (into [] (set (mapcat #(get-subtropes % tropes) tropes)))
        blocked-tropes (into [] (set (mapcat #(get-blocked-tropes % tropes) tropes)))
        bmake (fn [strope]
                (let [params (get-all-params strope)
                      inst (str (inst-start-name (:label strope))
                                (param-brackets (first (:events strope)) params))
                      fevent (first (:events strope))
                      ex (event-str fevent params)
                      cnds (param-str fevent params)]
                  (str inst " xinitiates\n" WS "perm(" ex ")" " if\n" WS WS (reduce str (interpose (str ",\n" WS WS) cnds)) ";\n\n")))

        tmake (fn [strope]
                (let [params (get-all-params strope)
                      inst (str (inst-stop-name (:label strope))
                                (param-brackets (first (:events strope)) params))
                      fevent (first (:events strope))
                      ex (event-str fevent params)
                      cnds (param-str fevent params)]
                  (str inst " xterminates\n" WS "perm(" ex ")" " if\n" WS WS (reduce str (interpose (str ",\n" WS WS) cnds)) ";\n\n")))
        cmake (fn [strope]
                (let [ex (event-str (first (:events strope)) (get-all-params strope))]
                  (str "cross fluent ipow(Trope, perm(" ex "), Trope);")))
        imake (fn [trope]
                (let [subs (get-subtropes trope tropes)
                      iname (event-name (:label trope))
                      enames (map #(perm (event-str (first (:events %)) (get-all-params %))) subs)
                      snames (map #(event-name (:label %)) subs)
                      ess (map vector enames snames)
                      is (map #(str "initially ipow (" iname ", " (first %) ", " (second %) ");") ess)
                      ]
                  (apply str (interpose "\n" is))))
        ;; imake (fn [strope])
        bridges (apply str (map bmake subtropes))
        blocked (apply str (map tmake blocked-tropes))
        crosses (apply str (map cmake subtropes))
        inits (apply str (map imake tropes))
        ]
    (apply str (concat crosses ["\n\n"] bridges ["\n\n"] blocked ["\n\n"] inits))))

;; (spit "resources/bridge-test.ial" (bridge [{:label "Quest" :events [{:verb "go" :role "hero" :place "away"}]} {:label "Hero's Journey" :events [{:verb "go" :role "hero" :place "home"} {:subtrope "Quest"}]}]))


(defn merge-lists [& maps]
  (reduce (fn [m1 m2]
            (reduce (fn [m [k v]]
                      (update-in m [k] (fnil concat []) v))
                    m1, m2))
          {}
          maps))

(defn norm-str [event params]
  (cond (:obligation event) (obl event params)
        (:permission event) (perm (event-str (:permission event) params))
      :else (perm (event-str event params))))

(defn initially [hmap]
  (let [
        header "\n% INITIALLY: -----------"
        params (apply merge (map get-all-params (:tropes hmap)))
        param-map (map get-all-params (:tropes hmap))
        obls (map get-obls (:tropes hmap))
        story (:story hmap)
        instances (:instances story)
        ;; role-list (mapcat #(map first (:roles %)) param-map)
        role-list (map :role (:characters hmap))
        ;; place-list (mapcat #(map first (:places %)) param-map)
        place-list (map :location (:places hmap))
        ;; obj-list (mapcat #(map first (:objects %)) param-map)
        obj-list (map :type (:objects hmap))
        first-events (map first (map :events (:tropes hmap)))
        ;; first-perms (map :perm (filter :perm first-events))
        ;; fperm-strs (map #(perm (event-str % params)) first-perms)
        fperm-strs (map #(str (norm-str %1 %2) " if " (reduce str (interpose ", " (param-str %1 %2)))) first-events param-map)
        ;; fperm-cnds (map #(param-str % params) first-events)

        fperms fperm-strs
        ;event-name?
        roles (filter #(in? role-list (:class %)) instances)
        places (filter #(in? place-list (:class %)) instances)
        objects (filter #(in? obj-list (:class %)) instances)
        fluentfn (fn [x t] (str t "(" (event-name (:iname x)) ", " (event-name (:class x)) ")"))
        rolestrs (map #(fluentfn % "role") roles)
        placestrs (map #(fluentfn % "place") places)
        objstrs (map #(fluentfn % "object") objects)
        ;; phasefn (fn [x] (str "phase(" x ", " INACTIVE ")"))
        phasefn (fn [x] (str "phase(" x ", " (str "phase" (first PHASES))  ")"))
        phases (map #(event-name (:label %)) (:tropes hmap))
        phasestrs (map phasefn phases)
        powifs (fn [letters] (reduce str (flatten (interpose ", " (map (partial interpose " != ") (partition 2 1 letters))))))
        powfn (fn [x] (let [letters (inst-letters x)
                            cnds (reduce str (flatten (interpose ", " (map #(interpose "!=" %) (partition 2 letters)))))]
                        (str "pow(" (inst-name (:label x))
                             "(" (reduce str (interpose ", " letters))
                             ;; ")) if " cnds)))
                             ;; "))"
                             ;; )))
                             ;; this one -->
                             ")) if " (powifs letters))))
        ;; test ["perm(go(lukeSkywalker,tatooine))"]
        situations (mapcat :situations (:tropes hmap))
        wpnames (map #(str "pow(" (inst-name (:verb (:when %))) "(" (reduce str (interpose ", " (sit-letters %))) "))") situations)
        opnames (map #(str "pow(" % ")") (mapcat :names obls))
        powers (map powfn (:tropes hmap))

        first-perms (reduce str (map #(str "initially\n    " (reduce str %) ";\n") fperms))
        ;; first-perms ""

        powstrs (reduce str (map #(str "initially\n    " (reduce str %) ";\n") powers))
        ;; powstrs ""
        ]

    ;; (concat rolestrs placestrs)
    ;; (concat role-list place-list)
    ;; roles
    ;; (map #(event-name (:class %)) instances)
    [header (str first-perms powstrs "initially\n    " (reduce str (interpose ",\n    " (concat wpnames opnames phasestrs rolestrs placestrs objstrs))) ";\n")]
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


(defn norm-params [ev params]
  (if (:obligation ev)  (mapcat #(param-str % params) [(:obligation ev) (:deadline (:obligation ev)) (:violation (:obligation ev))])
    (param-str ev params)))

(defn get-viols [trope]
  (let [obls (filter :obligation (:events trope))
        vs (:viols (get-obls trope))
        pevs (map :permission (filter :permission (map :violation (filter :violation (map :obligation obls)))))
        params (get-obl-params trope)
        ;; evs pevs
        evs (map #(perm (event-str % params)) pevs)
        vnames (map viol-name (filter #(:violation (:obligation %)) obls))
        conds (map #(param-str % params) pevs)
        ]
    {:names vnames :events [evs] :conds conds}))

(defn initiates [trope]
  (let [params (get-all-params trope)
        inst (str (inst-name (:label trope)) "(" (reduce str (interpose ", " (inst-letters trope))) ")")
        ename (event-name (:label trope))
        header (str "\n% INITIATES: " (namify (:label trope)) " ----------")
        term-header (str "% TERMINATES: " (namify (:label trope)) " ----------")
        ;; events (remove :obligation (:events trope))
        events (:events trope)
        imake (fn [iname evs cnds] (str iname " initiates\n" WS (reduce str (interpose (str ",\n" WS) (remove #(= "perm(())" %) evs))) " if\n" WS WS (reduce str (interpose (str ",\n" WS WS) cnds)) ";"))
        tmake (fn [iname evs cnds] (str iname " terminates\n" WS (reduce str (interpose (str ",\n" WS) (remove #(= "perm(())" %) evs))) " if\n" WS WS (reduce str (interpose (str ",\n" WS WS) cnds)) ";"))
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
        viols (get-viols trope)
        ;; tvec (conj phases [(last phases)])
        tvec (map vector phases)
        init-a (map imake (repeat inst) evec cvec)
        init-s (map imake (:names sits) (:events sits) (:conds sits))
        init-v (map imake (:names viols) (:events viols) (:conds viols))
        term-o (map tmake (:names obls) [(:evs obls)] (:conds obls))
        term-a (map tmake (repeat inst) (cons [(first phases)] (conj (into [] (map vector (rest phases) norms)) [(last phases)])) tvec)
        ]
    (concat [header] init-a init-s init-v ["\n"] [term-header] term-a term-o ["\n"])
    ;; (concat [header] init-a init-s init-v ["\n"])
    ))


(defn instal [hmap tropes]
  (let [;; initiallys [(str "initially\n    " (reduce str (interpose ",\n    " (mapcat #(initially % story) (:tropes hmap)))) ";")]
        initiallys (initially hmap)
        ;; initiallys []
        ;; inst-name [(str "institution " (event-name (:storyname (:story hmap))) ";")]
        inst-name [(str "institution " (event-name (:label (first (:tropes hmap)))) ";")]
        create ["% CREATION EVENT -----------" "create event startShow;\n"]
        exts (mapcat external-events (:tropes hmap))
        insts (mapcat #(inst-events % tropes) (:tropes hmap))
        ;; insts []
        obls (mapcat obl-events (:tropes hmap))
        inits (mapcat #(initiates %) (:tropes hmap))
        gens (mapcat #(generates % tropes) (:tropes hmap))
        viols (mapcat viol-events (:tropes hmap))
       ]
    ;; (get-params (first (:tropes hmap))))
    ;; (reduce str (interpose "\n" (concat types fluents exts ["\n"] insts ["\n"] inits ["\n"] gens))))
    (reduce str (interpose "\n" (concat inst-name types fluents exts viols insts obls inits gens initiallys))))
  )

(defn fix-crs [text]
  (clojure.string/replace text "\r" ""))

(defn instal-file [hmap tropes output]
  (do
    (spit output (instal hmap tropes))
    "true"))

(defn make-bridge [tropes]
  (let [bridge-name ["institution tropeBridge;\n"]
        bridge-text (bridge tropes)
        insts (mapcat #(inst-events % tropes) tropes)
        exts (mapcat external-events tropes)]
    (apply str (interpose "\n" (concat bridge-name types fluents ["\n"] insts ["\n"] exts ["\n"] [bridge-text])))))

(defn bridge-file [tropes output]
    (do
      (spit output (make-bridge tropes))
      "true"))

;; (defn instal-file [input output]
;;   (let [text (slurp input)
;;         result (instal-gen (fix-crs text))]
;;     (spit output result)))
