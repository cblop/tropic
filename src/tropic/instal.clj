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
  (str "int" (cap-first (event-name iname))))

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

(defn unify-params [params]
  (let [m (meta params)
        role (:subject params)
        obj (:object params)]
    (if (nil? obj)
      (if (nil? role) []
          [(str "role(X, " (event-name role) ")")])
      [(str "role(X, " (event-name role) ")") (str "object(Y, " (event-name obj) ")")])))


(defn generates [trope]
  (let [situations (:situations trope)
        wstrs (map #(event-str (:when %)) situations)
        wparams (map #(unify-params (:when %)) situations)
        gmake (fn [iname evs cnds] (str iname " generates " (reduce str (interpose ", " evs)) " if " (reduce str (interpose ", " cnds)) ";"))
        gen-a (map gmake wstrs (map #(vector (str "int" (cap-first (str %)))) wstrs) wparams)
        ]
    gen-a))

(defn initiates [trope roles objects]
  (let [inst (inst-name (:name trope))
        ename (event-name (:name trope))
        events (:events trope)
        situations (:situations trope)
        sitnorms (first (map :norms situations))
        wstrs (map #(event-str (:when %)) situations)
        wpvec (map #(perm (event-str (:permission %))) sitnorms)
        wpparams (map #(unify-params (:permission %)) sitnorms)
        wperms (map perm wstrs)
        estrs (map event-str events)
        perms (map perm estrs)
        wparams (map #(unify-params (:when %)) situations)
        params (map unify-params events)
        phases (make-phases ename (count events))
        mphases (butlast (rest phases))
        imake (fn [iname evs cnds] (str iname " initiates " (reduce str (interpose ", " evs)) " if " (reduce str (interpose ", " cnds)) ";"))
        evec (map vector mphases perms)
        cvec (map conj params phases)
        svec (map vector wperms)
        init-a (map imake (repeat inst) evec cvec)
        init-b (map imake (repeat inst) svec wparams)
        init-c (map imake (repeat (first (map #(str "int" (cap-first (str %))) wstrs))) (map vector wpvec) wpparams)
        ]
    ;; (imake (first evec) (first cvec))
    ;; (map imake (repeat inst) evec cvec)
    ;; (map imake (repeat inst) svec wparams)
    ;; (map imake (map inst-name wstrs) (map vector wpvec) wpparams)
    (concat init-a init-b init-c)
    ;; wpvec
    ;; events
    ))


(defn instal [hmap]
  (let [inits (mapcat initiates (:tropes hmap))
        gens (mapcat generates (:tropes hmap))]
    (reduce str (interpose "\n\n" (concat inits gens))))
  )

