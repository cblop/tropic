(ns tropic.instal
  (:require [clojure.string :as str]))

(def INACTIVE "inactive")
(def DONE "done")
(def PHASES ["A" "B" "C" "D" "E" "F"])
(def PARAMS ["X" "Y" "Z" "W"])

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
  (str "int" (cap-first (event-name iname)) "(X, Y)"))

(defn inst-name-h
  [iname]
  (str "int" (cap-first (event-name iname)) "(Agent, Object)"))

(defn event-str
  [event]
  (let [es (:predicate event)
        params (if (nil? (:object event))
                 [(:subject event)]
                 [(:subject event) (:object event)])
        met (zipmap params PARAMS)
        pstr (interpose ", " (take (count params) PARAMS))
        out (str es "(" (reduce str pstr) ")")
        ]
    (with-meta (symbol out) met)))

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
   "type Object;\n"])

(def fluents
  ["% FLUENTS ----------"
   "fluent role(Agent, Role);"
   "fluent phase(Trope, Phase);\n"])

(defn external-events [trope]
  (let [header (str "% EXTERNAL EVENTS: " (namify (:name trope)) " ----------")
        events (:events trope)
        situations (:situations trope)
        all (concat events situations)
        strng (fn [x] (str "external event " (event-str x) ";"))]
    (cons header (map strng all))))

(defn inst-events [trope]
  (let [header (str "% INST EVENTS: " (reduce str (:name trope)) " ----------")
        nm (inst-name-h (:name trope))
        instr (str "inst event " nm ";")]
    (cons header [instr])))

(defn terminates [trope roles objects]
  (let [inst (str (inst-name (:name trope)))]))


(defn initiates [trope roles objects]
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
  (let [exts (mapcat external-events (:tropes hmap))
        insts (mapcat inst-events (:tropes hmap))
        inits (mapcat #(initiates % (:roles hmap) (:objects hmap)) (:tropes hmap))
        gens (mapcat #(generates % (:roles hmap) (:objects hmap)) (:tropes hmap))]
    (reduce str (interpose "\n" (concat types fluents exts ["\n"] insts ["\n"] inits ["\n"] gens))))
  )

