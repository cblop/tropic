(ns tropic.instal
  (:require [clojure.string :as str]))

(def ACTIVE "active")
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
  [ev params]
  (let [event (or (:obligation ev) (:permission ev) ev)
        format (fn [xs]  (str "(" (reduce str (interpose ", " xs)) ")"))
        roles (map event-name (vals (select-keys event [:role :role-a :role-b :from :to])))
        objects (map event-name (remove #(or (= "Quest" %) (= "quest" %)) (concat (vals (select-keys (:deadline event) [:object])) (vals (select-keys event [:object])))))
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
  [ev params]
  (let [event (if (:permission ev) (:permission ev) ev)
        format (fn [xs]  (str (if (:verb event) (event-name (:verb event)) "") "(" (reduce str (interpose ", " xs)) ")"))
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
  (let [initial (str "phase(" ename ", " ACTIVE ")")
        phaser (fn [ch] (str "phase(" ename ", phase" ch ")"))
        end (str "phase(" ename ", " DONE ")")
        ps (map phaser (take len PHASES))]
    ;; (cons initial (conj (vec ps) end))
    (conj (vec ps) end)
    ))

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
    (str "viol" (reduce str name) "")))

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
        dead (if (nil? deadline) "intNoDeadline"
                 (str (inst-name (:verb deadline)) "(" (->> deadline
                                                (ev-types)
                                                (interpose ", ")
                                                (reduce str)
                                                ;; (reduce str (param-str params))
                                                ) ")"))
        viol (if (nil? violation) "noViolation"
                 (viol-name {:obligation obligation}))]
    (str "obl(" (inst-name (:verb obligation)) "(" obl "), " dead ", " viol ");")))

(defn obl [{:keys [obligation]} params]
  (let [deadline (:deadline obligation)
        violation (:violation obligation)
        obl (if (nil? obligation) ""
                (-> obligation
                    (event-str params)
                    ;; (param-str params)
                    ))
        dead (if (nil? deadline) "intNoDeadline"
                 (inst-name (event-str deadline params)))
        viol (if (nil? violation) "noViolation"
                 (viol-name {:obligation obligation})
                     ;; (param-str params)
                     )
        ]
    (str "obl(" (inst-name obl) ", " dead ", " viol ")")))

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
   ;; "fluent at(Agent, Place);
   "\n"])


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

(defn get-some-params [trope]
  (let [
        sits (map :when (filter :when (:situations trope)))
        perms (flatten (map #(map :permission (filter :permission %)) (map :norms (:situations trope))))
        eperms (map :permission (filter :permission (:events trope)))
        aperms (concat perms eperms)
        sobls (map :obligation (filter :obligation (:events trope)))
        obls sobls
        sdeads (map :deadline (map :obligation (filter :obligation (:events trope))))
        deads sdeads
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

(defn get-all-params [trope]
  (let [
        sits (map :when (filter :when (:situations trope)))
        ors (mapcat :or (filter :or (:events trope)))
        perms (flatten (map #(map :permission (filter :permission %)) (map :norms (:situations trope))))
        eperms (map :permission (filter :permission (:events trope)))
        operms (map :permission (filter :permission ors))
        aperms (concat perms eperms)
        sobls (map :obligation (filter :obligation (:events trope)))
        orobls (map :obligation (filter :obligation ors))
        obls (concat sobls orobls)
        sdeads (map :deadline (map :obligation (filter :obligation (:events trope))))
        ordeads (map :deadline (map :obligation (filter :obligation ors)))
        deads (concat sdeads ordeads)
        ;; wpvec (map (fn [x] (map #(perm (event-str (:permission %) sparams)) (filter :permission x))) sitnorms)
        evs (concat sits aperms obls deads ors (:events trope))
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


(defn extract-ifs [events]
  (let [ifs (mapcat :if (filter #(:if %) events))
        nifs (remove #(:if %) events)]
    (concat nifs ifs))
  )

(defn extract-ors [events]
  (let [ors (mapcat :or (filter #(:or %) events))
        nors (remove #(:or %) events)]
    (concat nors ors))
  )

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
        fall (concat events situations sperms)
        all (extract-ifs (extract-ors fall))
        types (map ev-types all)
        strng (fn [x y] (if (:verb x) (str "exogenous event " (event-name (:verb x)) "(" (reduce str (interpose ", " y)) ")" ";")))
        ]
    (concat (cons header (concat (into [] (set (map (fn [x y] (strng x y)) all types))) )) ["exogenous event noDeadline;"])
    ))
    ;; (prn-str types)
  ;; ))


(defn viol-events [trope]
  (let [header (str "\n% VIOLATION EVENTS: " (namify (:label trope)) " ----------")
        viols (filter :obligation (:events trope))
        strng (fn [x] (str "violation event " (viol-name x)";"))]
    (concat (cons header (into [] (set (map strng viols)))) ["violation event noViolation;"])))

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

(defn get-all-events [trope]
  (let [
        params (get-params trope)
        es (remove :obligation (:events trope))
        evs (map #(or (:permission %) %) es)
        deads (remove nil? (map #(-> % :obligation :deadline) (:events trope)))
        obls (remove nil? (map :obligation (:events trope)))
        events (concat evs obls deads)
        situations (map :when (:situations trope))
        sperms (mapcat #(map :permission (filter :permission %)) (map :norms (:situations trope)))
        fall (concat events situations sperms)
        all (extract-ifs (extract-ors fall))
        types (map ev-types all)
        istrng (fn [x y] (if (:verb x) (str "inst event " (inst-name (:verb x)) "(" (reduce str (interpose ", " y)) ")" ";")))
        ievs (into [] (set (map (fn [x y] (istrng x y)) all types)))]
    ievs)
  )

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
        istrng (fn [x y] (if (:verb x) (str "inst event " (inst-name (:verb x)) "(" (reduce str (interpose ", " y)) ")" ";")))
        ss (map stypes sparams)
        os (map stypes oparams)
        subss (map stypes subparams)
        finstr (fn [x ys] (str "inst event " x "(" (reduce str (interpose ", " ys)) ")" ";"))
        finstr-b (fn [x] (str "inst event " x ";"))
        instr (str "inst event " nm "(" (reduce str (interpose ", " types)) ")" ";")
        sinstrs (map finstr snms ss)
        oinstrs (map (fn [xs ys] (if (empty? ys) "" (finstr xs ys))) onms os)
        ;; subinstrs (map #(finstr (inst-start-name (:label %1)) %2) subs subss)
        subinstrs (map #(finstr-b (inst-start-name (:label %))) subs)
        ievs (get-all-events trope)
        ]
    (concat (cons header (conj (into [] (set (concat sinstrs oinstrs subinstrs ievs))) instr)) ["inst event intNoDeadline;"])))

(defn terminates [trope roles objects]
  (let [inst (str (inst-name (:label trope)))]))

;; (defn param-str [event params]
;;   (let [format (fn [x y] (str x "(" (reduce str (interpose ", " y)) ")"))
;;         ;; get roles, objects, places, quests for just this event
;;         roles (map event-name (vals (select-keys event [:role :role-a :role-b :from :to])))
;;         objects (map event-name (remove #(or (= "Quest" %) (= "quest" %)) (vals (select-keys event [:object]))))
;;         places (map event-name (vals (select-keys event [:place])))
;;         quests (map event-name (filter #(or (= "Quest" %) (= "quest" %)) (vals (select-keys event [:object]))))
;;         ;; format them into role(X, hero) strings by looking up their letters in params
;;         rstrs (map #(format "role" %) (map vector (map #(get-letter % (:roles params)) roles) roles))
;;         ostrs (map #(format "object" %) (map vector (map #(get-letter % (:objects params)) objects) objects))
;;         pstrs (map #(format "place" %) (map vector (map #(get-letter % (:places params)) places) places))
;;         qstrs (map #(format "quest" %) (map vector (map #(get-letter % (:quests params)) quests) quests))
;;         ]
;;     ;; put them in a nice list for processing
;;     (mapcat flatten [rstrs ostrs pstrs qstrs])
;;     ))


(defn inst-letters [trope]
  (let [params (get-all-params trope)
        num (reduce + [(count (:roles params))
                       (count (:objects params))
                       (count (:places params))
                       (count (:quests params))])]
    (take num PARAMS)))

(defn inst-params [trope]
  (let [params (get-all-params trope)
        roles (map #(str "role(" (second %) ", " (first %) ")") (:roles params))
        objects (map #(str "object(" (second %) ", " (first %) ")") (:objects params))
        places (map #(str "place(" (second %) ", " (first %) ")") (:places params))]
    (apply str (interpose ", " (apply concat [roles objects places])))))

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
                 (let [sub (:subtrope e)
                       phases (cons ACTIVE PHASES)
                       subtrope (first (filter #(or (= (:label %) (str "The " sub)) (= (:label %) sub)) tropes))]
                   (if (> i 0)
                     {:subtrope subtrope
                      :phase (nth phases (dec i))
                      :trigger (nth (:events trope) (dec i))}
                     {:subtrope subtrope}))) (:events trope)))

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
        p (println "SUBS2:")
        p (println (prn-str subs))
        header (str "% GENERATES: " (reduce str (:label trope)) " ----------")
        inst (str (inst-name (:label trope)) "(" (reduce str (interpose ", " (inst-letters trope))) ")")
        situations (:situations trope)
        wnames (map #(str (inst-name (:verb (:when %))) "(" (reduce str (interpose ", " (sit-letters %))) ")") situations)
        onames (map #(str (inst-name (:verb %)) "(" (reduce str (interpose ", " (lookup-obl-letters trope %))) ")") oevs)
        ename (event-name (:label trope))
        events (extract-ors (remove :obligation (:events trope)))
        wstrs (map (fn [x ys] (event-str (:when x) ys)) situations wparams)
        ostrs (remove #(= "()" %) (into [] (set (map #(event-str % oparams) oevs))))
        gmake (fn [iname ev cnds] (if-not (= "()" ev) (str ev " generates\n" WS iname " if\n" WS WS (reduce str (interpose (str ",\n" WS WS) cnds)) ";")))
        imake (fn [ev cnds] (if-not (= "()" ev) (str ev " generates\n" WS (inst-name ev) " if\n" WS WS (reduce str (interpose (str ",\n" WS WS) cnds)) ";")))
        estrs (map #(event-str % params) events)
        pstrs (map #(param-str % params) events)
        ;; opstrs (map #(param-str % oparams) oevs)
        wifs (map (fn [x ys] (param-str x ys)) (map :when (filter :when situations)) wparams)
        oifs (remove #(= "()" %) (map #(param-str % oparams) oevs))
        ;; smake (fn [sub]
        ;;         (if (:subtrope sub)
        ;;           (let [pms (get-all-params (assoc trope :events (concat (:events trope) (:events (:subtrope sub)))))
        ;;                 int (event-name (:label trope))
        ;;                 ]
        ;;             (gmake (str (inst-start-name (:label (:subtrope sub))) (param-brackets (first (:events (:subtrope sub))) pms)) (event-str (:trigger sub) pms) (concat (param-str (first (:events (:subtrope sub))) pms) (param-str (:trigger sub) pms) [(str "phase(" int ", " "phase" (:phase sub) ")")]))
        ;;             )))
        smake (fn [sub]
                (if (:subtrope sub)
                  (let [pms (get-all-params (assoc trope :events (concat (:events trope) (:events (:subtrope sub)))))
                        int (event-name (:label trope))
                        ]
                    (gmake (str (inst-start-name (:label (:subtrope sub)))) (event-str (:trigger sub) pms) (concat (param-str (:trigger sub) pms) [(str "phase(" int ", " (if (= "active" (:phase sub)) "active" (str "phase" (:phase sub))) ")")]))
                    )))
        gen-subs (remove nil? (map smake subs))
        gen-a (into [] (set (map gmake (repeat inst) estrs pstrs)))
        gen-i (into [] (set (map imake estrs pstrs)))
        p (println "OS:")
        p (println ostrs)
        p (println oifs)
        gen-o (into [] (set (map imake ostrs oifs)))
        gen-s (map gmake wnames wstrs wifs)
        gen-d (map (fn [w x y z] (if (empty? w) "" (gmake x y z))) deads onames ostrs oifs)
        ]
    ;; not sure why I had gen-d (obligations) in there
    ;; what the hell was gen-i about?
    (concat [header] gen-subs gen-a gen-s gen-o)
    ))


(defn bridge [tropes]
  (let [;; ievents (subs-triggers tropes)
        p (println tropes)
        source (str "source " (event-name (:label (first tropes))) ";")
        sink (str "sink " (event-name (:label (second tropes))) ";")
        ;; subtropes (into [] (set (mapcat #(get-subtropes % tropes) tropes)))
        subtropes [(second tropes)]
        blocked-tropes (into [] (set (mapcat #(get-blocked-tropes % tropes) tropes)))
        bmake (fn [strope]
                (let [params (get-all-params strope)
                      inst (str (inst-start-name (:label strope))
                                ;; (param-brackets (first (:events strope)) params)
                                )
                      fevent (first (:events strope))
                      ex (if (:obligation fevent) (str "obl(" (event-str (:obligation fevent) params) ", " (event-str (:deadline (:obligation fevent)) params) ", " (viol-name fevent) ")")
                             (str "perm(" (event-str fevent params) ")"))
                      cnds (param-str fevent params)
                      initphase (str inst " xinitiates phase(" (event-name (:label strope)) ", " ACTIVE ");")
                      initperm (str inst " xinitiates " ex " if\n" WS WS (apply str (interpose (str ",\n" WS WS) cnds)) ";\n\n")]
                  ;; (str inst " xinitiates\n" WS ex ", phase(" (event-name (:label strope)) ", active)" " if\n" WS WS (reduce str (interpose (str ",\n" WS WS) cnds)) ";\n\n")
                  ;; (str inst " xinitiates active;\n\n")
                  (str initphase "\n" initperm)
                  ))

        tmake (fn [strope]
                (let [params (get-all-params strope)
                      inst (str (inst-stop-name (:label strope))
                                (param-brackets (first (:events strope)) params))
                      fevent (first (:events strope))
                      ex (event-str fevent params)
                      cnds (param-str fevent params)]
                  (str inst " xterminates\n" WS "perm(" ex ")" " if\n" WS WS (reduce str (interpose (str ",\n" WS WS) cnds)) ";\n\n")))

        cmake (fn [strope]
                (let [params (get-all-params strope)
                      fevent (first (:events strope))
                      types (ev-types fevent)
                      ex (if (:obligation fevent) (str "obl(" (event-str (:obligation fevent) params) ", " (event-str (:deadline (:obligation fevent)) params) ", " (viol-name fevent) ")")
                             (str "perm(" (event-name (:verb fevent)) "(" (apply str (interpose ", " types)) "))"))]
                  (str "cross fluent ipow(" (event-name (:label (first tropes))) ", " ex ", "(event-name (:label (second tropes))) ");\ncross fluent ipow(" (event-name (:label (first tropes))) ", phase(Trope, Phase), " (event-name (:label (second tropes))) ");")));")))

        imake (fn [ts]
                (let [trope (first ts)
                      subs [(second ts)]
                      iname (event-name (:label trope))
                      enames (map #(if (:obligation (first (:events %))) (obl (first (:events %)) (get-all-params %)) (perm (event-str (first (:events %)) (get-all-params %)))) subs)
                      snames (map #(event-name (:label %)) subs)
                      ess (map vector enames snames)
                      is (map #(str "initially ipow(" iname ",  " (first enames) ", " (second %) "),\n    ipow(" iname ", phase(" (second %) ", active), " (second %) ");\n") ess)
                      ]
                  (apply str (interpose "\n" is))))
        ;; imake (fn [strope])
        ;; bridges (apply str (map bmake subtropes))
        bridges (bmake (second tropes))
        blocked (apply str (map tmake blocked-tropes))
        crosses (apply str (map cmake subtropes))
        inits (imake tropes)
        ]
    (apply str (concat source ["\n\n"] sink ["\n\n"] crosses ["\n\n"] bridges ["\n\n"] blocked ["\n\n"] inits))))

;; (spit "resources/bridge-test.ial" (bridge [{:label "Quest" :events [{:verb "go" :role "hero" :place "away"}]} {:label "Hero's Journey" :events [{:verb "go" :role "hero" :place "home"} {:subtrope "Quest"}]}]))


(defn merge-lists [& maps]
  (reduce (fn [m1 m2]
            (reduce (fn [m [k v]]
                      (update-in m [k] (fnil concat []) v))
                    m1, m2))
          {}
          maps))

(defn norm-str [event params]
  (cond
    ;; (:subtrope event) (str "pow(" (inst-start-name (:subtrope event)))
    (:or event) (apply str (interpose ",\n    " (map #(norm-str % params) (:or event))))
    (:obligation event) (obl event params)
        (:permission event) (perm (event-str (:permission event) params))
      :else (perm (event-str event params))))

(defn initially [hmap tropes]
  (let [
        header "\n% INITIALLY: -----------"
        params (apply merge (map get-all-params (:tropes hmap)))
        param-map (map get-all-params (:tropes hmap))
        obls (map get-obls (:tropes hmap))
        story (:story hmap)
        instances (:instances story)
        ;; subs (mapcat #(subs-triggers (first (:tropes hmap)) %) tropes)
        subs (subs-triggers (first (:tropes hmap)) tropes)
        p (println "TROPES:")
        p (println tropes)
        p (println "HMAP:")
        p (println (:tropes hmap))
        ;; p (println (prn-str subs))
        subints (remove nil? (map #(if (:subtrope %) (inst-start-name (:label (:subtrope %)))) subs))
        ;; role-list (mapcat #(map first (:roles %)) param-map)
        role-list (map :role (:characters hmap))
        ;; place-list (mapcat #(map first (:places %)) param-map)
        place-list (map :location (:places hmap))
        ;; obj-list (mapcat #(map first (:objects %)) param-map)
        obj-list (map :type (:objects hmap))
        first-events (map (fn [x] (if (:or (first x)) (first (:or (first x))) (first x))) (map :events (:tropes hmap)))
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
        starting (some #(= (event-name (:label (first (:tropes hmap)))) %) (:starters hmap))
        phasefn (fn [x] (if starting (str "phase(" x ", " ACTIVE ")")))
        ;; phasefn (fn [x] (str "phase(" x ", " (str "phase" (first PHASES))  ")"))
        phases (map #(event-name (:label %)) (:tropes hmap))
        phasestrs (remove nil? (map phasefn phases))
        powifs (fn [letters] (reduce str (flatten (interpose ", " (map (partial interpose " != ") (partition 2 1 letters))))))
        permfn (fn [x] (let [letters (inst-letters x)
                            cnds (reduce str (flatten (interpose ", " (map #(interpose "!=" %) (partition 2 letters)))))]
                        (str "perm(" (inst-name (:label x))
                             "(" (reduce str (interpose ", " letters))
                             ;; ")) if " cnds)))
                             ;; "))"
                             ;; )))
                             ;; this one -->
                             ;; ")) if " (powifs letters))))
                             ")) if " (inst-params x))))
        powfn (fn [x] (let [letters (inst-letters x)
                            cnds (reduce str (flatten (interpose ", " (map #(interpose "!=" %) (partition 2 letters)))))]
                        (str "pow(" (inst-name (:label x))
                             "(" (reduce str (interpose ", " letters))
                             ;; ")) if " cnds)))
                             ;; "))"
                             ;; )))
                             ;; this one -->
                             ;; ")) if " (powifs letters))))
                             ")) if " (inst-params x))))
        ;; test ["perm(go(lukeSkywalker,tatooine))"]
        situations (mapcat :situations (:tropes hmap))
        wpnames (map #(str "pow(" (inst-name (:verb (:when %))) "(" (reduce str (interpose ", " (sit-letters %))) "))") situations)
        opnames (map #(str "pow(" % ")") (mapcat :names obls))
        powers (concat (map #(str "pow(" % ")") subints) (map powfn (:tropes hmap)))
        perms (concat (map #(str "perm(" % ")") subints) (map permfn (:tropes hmap)))
        ;; active (if (some #(= (event-name (:label (first (:tropes hmap)))) %) (:starters hmap)) (str "active,\n    perm(start(" (event-name (:label (first (:tropes hmap)))) ")),\n    pow(intStart),\n    perm(intStart),\n    ") "")

        first-perms (if (some #(= (event-name (:label (first (:tropes hmap)))) %) (:starters hmap)) (reduce str (map #(str "initially\n    " (reduce str %) ";\n") fperms)) "")
        ;; first-perms ""

        powstrs (reduce str (map #(str "initially\n    " (reduce str %) ";\n") powers))
        permstrs (reduce str (map #(str "initially\n    " (reduce str %) ";\n") perms))
        ;; powstrs ""

        ;; startstrs (map #(str "perm(start(" (event-name (:label %)) "))") (:tropes hmap))
        ;; intstartstrs ["pow(intStart)" "perm(intStart)"]
        ]

    ;; (concat rolestrs placestrs)
    ;; (concat role-list place-list)
    ;; roles
    ;; (map #(event-name (:class %)) instances)
    ;; removed first-perms
    [header (str powstrs permstrs first-perms "initially\n    " (reduce str (interpose ",\n    " (concat wpnames opnames phasestrs rolestrs placestrs objstrs)))";\n")]
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
  (cond
    (:obligation ev) (mapcat #(param-str % params) [(:obligation ev) (:deadline (:obligation ev)) (:violation (:obligation ev))])
    (:or ev) (seq (set (mapcat #(norm-params % params) (:or ev))))
    :else (param-str ev params)))

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
        events (rest (:events trope))
        imake (fn [iname evs cnds] (str iname " initiates\n" WS (reduce str (interpose (str ",\n" WS) (remove #(= "perm(())" %) evs))) (if (seq (remove nil? cnds)) (str " if\n" WS WS (reduce str (interpose (str ",\n" WS WS) cnds))) "") ";"))
        tmake (fn [iname evs cnds] (str iname " terminates\n" WS (reduce str (interpose (str ",\n" WS) (remove #(= "perm(())" %) evs))) (if (seq (remove nil? cnds)) (str " if\n" WS WS (reduce str (interpose (str ",\n" WS WS) cnds))) "") ";"))
        ;; estrs (map #(event-str % params) events)
        estrs (map #(norm-str % params) events)
        pstrs (map #(norm-params % params) events)
        ;; perms (map perm estrs)
        ;; oblis (map #(obl % params) (filter :obligation (:events trope)))
        ;; norms (concat perms oblis)
        norms estrs
        ;; norms perms
        phases (make-phases ename (count events))
        evec (into [] (map vector phases norms))
        ;; evec (conj (into [] (map vector (rest phases) norms)) [(last phases)])
        cvec (conj (into [] (map conj pstrs (cons (str "phase(" (event-name (:label trope)) ", " ACTIVE ")") phases))) [(last (butlast (rest phases)))])
        ;; cvec (conj (into [] (map conj pstrs phases)) [(last (butlast (rest phases)))])
        sits (get-sits trope)
        obls (get-obls trope)
        viols (get-viols trope)
        ;; tvec (conj phases [(last phases)])
        ;; tvec (map conj pstrs phases)
        ;; tvec (cons [(first phases)] (into [] (map conj pstrs (rest phases))))
        active (str "phase(" (event-name (:label trope)) ", " ACTIVE ")")
        tfirst (norm-params (first (:events trope)) params)
        efirst (norm-str (first (:events trope)) params)
        ;; tvec (into [] (map conj (cons tfirst pstrs) (cons active phases)))
        tvec (into [] (map conj (cons tfirst pstrs) (cons active phases)))
        init-a (map imake (repeat inst) evec cvec)
        init-s (map imake (:names sits) (:events sits) (:conds sits))
        init-v (map imake (:names viols) (:events viols) (:conds viols))
        term-o (map tmake (:names obls) [(:evs obls)] (:conds obls))
        ;; term-a (map tmake (repeat inst) (cons [(first phases)] (conj (into [] (map vector (rest phases) norms)) [(last phases)])) tvec)
        ;; term-a (map tmake (repeat inst) (into [] (map vector phases (cons efirst norms))) tvec)
        term-a (map tmake (repeat inst) (into [] (map vector (cons active phases) (cons efirst norms))) tvec)
        ;; term-start [(str "intStart terminates perm(start(" (event-name (:label trope)) ")), perm(intStart), pow(intStart);\n")]
        ]
    (concat [header] init-a init-s init-v [term-header] term-a term-o ["\n"])
    ;; (concat [header] init-a init-s init-v ["\n"])
    ))


(defn instal [hmap tropes]
  (let [;; initiallys [(str "initially\n    " (reduce str (interpose ",\n    " (mapcat #(initially % story) (:tropes hmap)))) ";")]
        initiallys (initially hmap tropes)
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

;; (defn make-bridge [tropes]
;;   (if (> (count tropes) 1)
;;     (for [trope tropes]
;;       (let [subtropes (into [] (set (get-subtropes trope)))]
;;         (for [subtrope subtropes]
;;           (let [bridge-name (event-name (str "bridge " (:label trope) " " (:label subtrope)))
;;                 bridge-dec [(str "bridge " bridge-name ";\n")]
;;                 bridge-text (bridge [trope subtrope])]))
;;         (apply str (interpose "\n" (concat bridge-name ["\n"] [bridge-text])))
;;         ))
;;     ""
;;     ))

(defn make-bridge [tropes]
  (let [
        bridge-name [(str "bridge " (event-name (str (:label (first tropes)) " " (:label (second tropes)))) ";\n")]
        bridge-text (bridge tropes)
        insts (mapcat #(inst-events % tropes) tropes)
        exts (mapcat external-events tropes)
        viols (mapcat viol-events tropes)]
    ;; (apply str (interpose "\n" (concat bridge-name types fluents ["\n"] insts ["\n"] exts ["\n"] viols ["\n"] [bridge-text])))
    (apply str (interpose "\n" (concat bridge-name ["\n"] [bridge-text])))
    )
  ;; ""
  )

(defn bridge-file [tropes output]
    (do
      (spit output (make-bridge tropes))
      "true"))

(defn bridge-files [tropes output]
  (println "hey")
  (println (prn-str tropes))
  (doseq [trope tropes]
    (do
      (println (prn-str trope))
      (let [subtropes (into [] (set (get-subtropes trope tropes)))]
        (println (str "BRIDGE: " (prn-str subtropes)))
        (doseq [subtrope subtropes]
          (let [bridge-name (event-name (str (:label trope) " " (:label subtrope)))]
            ;; (spit (str output bridge-name ".ial") (make-bridge [trope subtrope]))
            (println (str "SUBTROPE: " (prn-str subtrope)))
            (bridge-file [trope subtrope] (str output bridge-name "-bridge.ial"))
            )))))
  )

;; (defn instal-file [input output]
;;   (let [text (slurp input)
;;         result (instal-gen (fix-crs text))]
;;     (spit output result)))
