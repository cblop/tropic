(ns tropic.query
  (:require [me.raynes.conch :refer [programs with-programs let-programs] :as sh])
  (:require [clojure.java.io :refer [file]])
  (:require [clojure.string :as str]))

(programs cat python2 python clingo)

;; yeah, change this
;; and all the starWars stuff so it can generalise
(def model (file "resources/test4.ial"))

(defn make-query-string [event]
  (let [ag (:AGENT event)
        functor (:FUNCTOR event)
        vs (:VALUE event)]
    (if (= ag "inst")
      (str functor "(" (str/join "," vs) ")")
      (str functor "(" (str/join "," (cons ag vs)) ")"))
     ;(str functor "(" (str/join "," (cons ag vs)) ")")
    ))

(defn make-query [q]
  (let [post (for [x (vec (range (count q)))
                 :let [y (str "observed(" (nth q x) ",starWars," (+ 1 x) ").")]]
               y)
        post-string (str/join "\n" post)]
    (spit "resources/query.lp" (str "observed(startShow,starWars,0).\n" post-string))))

(defn make-timeline [qlength] (spit "resources/timeline.lp" (str "start(0).\ninstant(0..T) :- final(T).\nnext(T,T+1) :- instant(T).\nfinal(" qlength ").")))

(defn run-instal [] (python2 "instal/pyinstal.py" "-d" "resources/domain.idc" "-i" "resources/test4.ial" "-o" "resources/test4.lp"))

(defn run-clingo [] (clingo "resources/test4.lp" "resources/timeline.lp" "resources/query.lp" {:out (file "resources/results.txt") :throw false}))

(defn run-query [q]
  (do
    (make-query q)
    (make-timeline (+ 1 (count q)))
    (run-instal)
    (run-clingo)))

(defn get-state [qlength]
  (let [strip-lives (fn [x] (remove #(re-matches #".*live.*" %) x))
        res (-> (slurp "resources/results.txt")
               (str/split #" "))]
    (strip-lives (filter #(re-matches (re-pattern (str "holdsat..*.," qlength ".")) %) res))))

(defn get-obls [state]
  (filter #(.contains % "obl(") state))

(defn get-perms [state]
  (->> state
      (filter #(.contains % "perm("))
      (remove #(.contains % "null"))))

(defn get-viols [state]
  (->> state
      (filter #(.contains % "viol("))
      (remove #(.contains % "null"))))


(defn get-fluents [state]
  (remove #(or (.contains % "perm(") (.contains % "obl(") (.contains % "pow(")) state))

(defn get-stage [state]
  (filter #(.contains % "onStage(") state))

(defn get-tropes [state]
  (filter #(.contains % "activeTrope(") state))

(defn get-pows [state]
  (filter #(.contains % "pow(") state))

(defn strip-fluff [s]
  (-> s
  (str/replace "holdsat(" "")
  (str/replace #",starWars,.." "")))

(defn filter-results [length]
  (let [state (get-state length)]
      (hash-map :fluents (map strip-fluff (get-fluents state)) :tropes (map strip-fluff (get-tropes state)) :onstage (map strip-fluff (get-stage state))  :obligations (map strip-fluff (get-obls state)) :permissions (map strip-fluff (get-perms state)) :violations (map strip-fluff (get-viols state)))))

(defn norms-for-query [query]
  (let [qlength (+ 1 (count query))]
  (do (run-query query)
      (filter-results qlength))))

(defn norms-at-state [index]
  (let [i (+ 1 index)]
      (filter-results i)))

