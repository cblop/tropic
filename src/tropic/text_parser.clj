(ns tropic.text-parser
  (:require [instaparse.core :as insta]
            [damionjunk.nlp.cmu-ark :as ark]
            ;; [damionjunk.nlp.stanford :as stan]
            [tropic.instal :refer [event-name]]
            [clojure.string :as str]))

(def solver-parser
  (insta/parser
   "output = observation* final <end>?
    final = observation
    <observation> = (observed <'\n'>)+ <'\n'>
    observed = (<'holdsat('> norm+ <')'>) | (<'occurred('> (event / v-event)+ <')'>)
    norm = (perm / obl / pow / live / fluent) <','> inst <','> instant
    perm = <'perm('> word [<'('> params <')'>] <')'>
    obl = <'obl('> obl-event <','> deadline <','> viol<')'>
    pow = <'pow('> inst <','> word [<'('> params <')'>] <')'>
    live = <'live('> word [<'('> params <')'>] <')'>
    fluent = word [<'('> params <')'>]
    event = word [<'('> params <')'>]<','> inst <','> instant
    obl-event = word [<'('> params <')'>]
    deadline = word [<'('> params <')'>]
    viol = word [<'('> params <')'>]
    <v-event> = <'viol(' <viol> '),' inst ',' instant>
    inst = word
    end = <'\n'>* <'Passed(' number ')'> <'\n'>*
    params = word (<','> word)*
    instant = number
    <word> = #'[a-zA-Z\\-\\_\\']+'
    <number> = #'[0-9]+'
    <words> = word (<' '> word)*"))


(defn solve-parse [text]
  (insta/add-line-and-column-info-to-metadata
   text
   (solver-parser text)))

;; (solve-parse (slurp "resources/output.txt"))

;; (solve-parse
;;  (str
;;   "holdsat(in_fact(bar),basic,2)\n"
;;   "holdsat(perm(in_red(bar)),basic,2)\n"
;;   "holdsat(in_fact(foo),basic,1)\n"
;;   "holdsat(perm(in_red(foo)),basic,1)\n"
;;   "holdsat(obl(ex_red(foo),ex_green(foo),ex_blue(foo)),basic,1)\n"
;;   "holdsat(pow(basic,in_blue(foo)),basic,1)\n"
;;   "holdsat(live(basic),basic,1)\n"
;;   "occurred(in_red(foo),basic,0)\n"
;;   "occurred(ex_red(foo),basic,0)"))

(defn parse-int [s]
  (Integer/parseInt (re-find #"\A-?\d+" s)))


(defn get-if-key [key xs]
  (filter #(get % key) xs))

(defn transform
  [ptree]
  (insta/transform
   {:instant (fn [& args] {:instant (parse-int (first args))})
    :inst (fn [& args] {:inst (first args)})
    :fluent (fn [& args] (apply merge (conj (rest args) {:fluent (first args)})))
    :perm (fn [& args] (apply merge (conj (rest args) {:perm (first args)})))
    :pow (fn [& args] {:pow (first args)})
    :viol (fn [& args] {:viol (first args)})
    :deadline (fn [& args] {:deadline (first args)})
    :obl-event (fn [& args] (apply merge (conj (rest args) {:event (first args)})))
    :event (fn [& args] (apply merge (conj (rest args) {:event (first args)})))
    :live (fn [& args] {:live (first args)})
    :params (fn [& args] {:params args})
    :norm (partial merge)
    :obl (fn [& args] {:obl (apply merge args)})
    :observed (fn [& args] (first args))
    :final (fn [& args] args)
    :output (fn [& args] (hash-map
                          :perms (into [] (sort-by :instant (get-if-key :perm args)))
                          :fluents (into [] (sort-by :instant (get-if-key :fluent args)))
                          :events (into [] (sort-by :instant (get-if-key :event args)))
                          :pows (into [] (sort-by :instant (get-if-key :pow args)))
                          :obls (into [] (sort-by :instant (get-if-key :obl args)))))
    }
   ptree))

;; (-> (str
;;      "holdsat(in_fact(bar),basic,2)\n"
;;      "holdsat(perm(in_red(bar)),basic,2)\n"
;;      "holdsat(in_fact(foo),basic,1)\n"
;;      "holdsat(perm(in_red(foo)),basic,1)\n"
;;      "holdsat(obl(ex_red(foo),ex_green(foo),ex_blue(foo)),basic,1)\n"
;;      "holdsat(pow(basic,in_blue(foo)),basic,1)\n"
;;      "holdsat(live(basic),basic,1)\n"
;;      "occurred(in_red(foo),basic,0)\n"
;;      "occurred(ex_red(foo),basic,0)")
;;     (solve-parse)
;;     (transform))

(defn snth [coll n]
  (if (< (count coll) (+ n 1)) nil
      (nth coll n)))

(defn get-for-instant [hmap i]
  (filter #(= (:instant %) i) hmap))

(defn embellish [word]
  (->> word
       (split-with #(not (Character/isUpperCase %)))
       (map #(clojure.string/capitalize (apply str %)))
       (interpose " ")
       (reduce str)
       (clojure.string/trim))
  )

(defn say-options [hmap]
  (let [permfn (fn [p] (cond (nil? p) nil
                             (= (:perm p) "null") nil
                             (= (count (:params p)) 1) (str (embellish (first (:params p))) " can " (embellish (:perm p)) ".")
                             :else (str (embellish (first (:params p))) " can " (embellish (:perm p)) " the " (embellish (second (:params p))) ".")
                             ))
        oblfn (fn [x] (let [o (:obl x)
                            ev (cond (nil? o) nil
                                     (= (count (:params o)) 1) (str (embellish (first (:params o))) " must " (embellish (:event o)))
                                     :else (str (embellish (first (:params o))) " must " (embellish (:perm o)) " the " (embellish (second (:params o))))
                                     )]
                        (cond
                          (nil? ev) ev
                          (and (nil? (:viol o)) (nil? (:deadline o))) (str (embellish ev) ".")
                          (nil? (:viol o)) (str (embellish ev) " before " (embellish (:deadline o)))
                          :else (str (embellish ev) " before " (embellish (:deadline o)) ", otherwise " (embellish (:viol o)) ".")
                          )))
        fluentfn (fn [f] (cond (nil? f) nil
                               (= (:fluent f) "null") nil
                               (nil? (:params f)) (str (embellish (:fluent f)) " is true.")
                               (= (count (:params f)) 1) (str (embellish (:fluent f)) " is " (embellish (first (:params f))))
                               :else (str (embellish (first (:params f))) "'s " (:fluent f) " is " (embellish (second (:params f))))
                               ))

        ;; p (println hmap)
        now (last (sort (mapcat #(map :instant %) (vals hmap))))
        perms (map permfn (get-for-instant (:perms hmap) now))
        obls (map oblfn (get-for-instant (:obls hmap) now))
        fluents (map fluentfn (get-for-instant (:fluents hmap) now))
        ]
    (reduce str (interpose "\n" (concat fluents perms obls)))
    ))

(defn trace-to-prose [trace]
  (-> trace
      (solve-parse)
      (transform)
      (say-options)))


(-> (slurp "resources/output.txt")
    (solve-parse)
    (transform)
    ;; (say-options)
    )


;; (-> (str
;;      "holdsat(obl(ex_red(bar),ex_green(bar),ex_blue(bar)),basic,2)\n"
;;      "holdsat(in_fact(bar),basic,2)\n"
;;      "holdsat(perm(in_red(bar)),basic,2)\n"
;;      "holdsat(in_fact(foo),basic,1)\n"
;;      "holdsat(perm(in_red(foo)),basic,1)\n"
;;      "holdsat(obl(ex_red(foo),ex_green(foo),ex_blue(foo)),basic,1)\n"
;;      "holdsat(pow(basic,in_blue(foo)),basic,1)\n"
;;      "holdsat(live(basic),basic,1)\n"
;;      "occurred(in_red(foo),basic,0)\n"
;;      "occurred(ex_red(foo),basic,0)")
;;     (solve-parse)
;;     (transform)
;;     (say-options))


(defn make-ark-tree [tags]
  (into [] (remove nil? (map (fn [{:keys [token pos]}]
                               (cond (= pos "V") [:verb token]
                                     (= pos "N") [:object token]
                                     (= pos "^") [:character token]))
                             tags))))

;; STEPS:
;; 1. POS-tag
;; 2. Replace/format char/object names
;; 3. Compare against solver output

(defn format-chars [text]
  (letfn [(combine [words]
            (if (> (count words) 1) [(first (first words)) (event-name (reduce str (interpose " " (map #(clojure.string/capitalize (second %)) words))))]
                (first words)))]
    (map combine (partition-by first text))))

(defn nlp-parse [text]
  (-> text
      (ark/tag)
      (make-ark-tree)
      (format-chars)))

(defn observe [text inst n]
  (let [ptree (nlp-parse text)
        hmap (apply hash-map (apply concat ptree))
        event (interpose "," (remove nil? [(:character hmap) (:object hmap)]))
        evf (if (empty? event) "" (reduce str (cons "," event)))
        ]
    ;; (str "observed(" (:verb hmap) "(player" evf ")," inst "," n ")")
    (str "observed(" (:verb hmap) "(lukeSkywalker" evf ")," inst")")
    ))

;; (nlp-parse "give luke skywalker the light saber")
;; (observe (nlp-parse "give luke skywalker the light saber") "starWars" 1)
;; (ark/tag "talk to Luke Skywalker")


;; (ark/tag "look at the phone")
;; (make-tree (pos-tag (tokenize "go to the zoo")))
;; (make-tree (pos-tag (tokenize "throw the chair away")))
;; (make-tree (pos-tag (tokenize "go up")))
;; (make-tree (pos-tag (tokenize "look at the phone")))
;; (pos-tag (tokenize "go to the zoo"))
;; (pos-tag (tokenize "go north"))
;; (pos-tag (tokenize "look at the phone"))
;; (pos-tag (tokenize "examine the phone"))