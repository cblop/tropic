(ns tropic.text-parser
  (:require [instaparse.core :as insta]
            ;; [damionjunk.nlp.cmu-ark :as ark]
            ;; [damionjunk.nlp.stanford :as stan]
            [tropic.instal :refer [event-name]]
            [clojure.string :as str]))

(def solver-parser
  (insta/parser
   "output = <observation>* final
    final = observation
    <observation> = (observed <'\n'>)+ <'\n'>+
    observed = (<'holdsat('> norm+ <')'>) | (<'occurred('> (event / v-event)+ <')'>)
    norm = (perm / obl / pow / ipow / live / fluent) <',' inst>
    perm = <'perm('> word [<'('> params <')'>] <')'>
    obl = <'obl('> obl-event <','> deadline <','> viol<')'>
    pow = <'pow('> inst [<'('> params <')'>] <')'>
    ipow = <'ipow('> inst <','> (perm / obl / (word [<'('> params <')'>])) <','> inst <')'>
    live = <'live('> word [<'('> params <')'>] <')'>
    fluent = word [<'('> params <')'>]
    event = word [<'('> params <')'>]<',' inst>
    obl-event = word [<'('> params <')'>]
    deadline = word [<'('> params <')'>]
    viol = word [<'('> params <')'>]
    <v-event> = <'viol(' <viol> '),' inst>
    <inst> = word
    end = <'\n'>* <'Passed(' number ')'> <'\n'>*
    params = word (<','> word)*
    <instant> = number
    <word> = #'[a-zA-Z\\-\\_\\']+'
    <number> = #'[0-9]+'
    <words> = word (<' '> word)*
"))

(def query-parser
  (insta/parser
   "output = set-no <'\\n'>+ step+
    set-no = <'Answer Set '> number <':'>
    step = (step-no <'\\n'>+ facts <'\\n'>*)
    step-no = <'Time Step '> number <':'>
    facts = ((<null> / observed / occurred / holds) <'\\n'>)+
    <null> = ('observed' | 'occurred' | 'holdsat') <'(null,'> <inst>
    observed = <'observed('> event <')'>
    occurred = <'occurred('> (event | viol) <')'>
    holds = (<'holdsat('> norm+ <')'>)
    norm = (perm / obl / pow / ipow / live / fluent) <',' inst>
    perm = <'perm('> word [<'('> params <')'>] <')'>
    obl = <'obl('> obl-event <','> deadline <','> consequence <')'>
    pow = <'pow('> inst [<'('> params <')'>] <')'>
    ipow = <'ipow('> inst <','> (perm / obl / (word [<'('> params <')'>])) <','> inst <')'>
    live = <'live('> word [<'('> params <')'>] <')'>
    fluent = word [<'('> params <')'>]
    event = word [<'('> params <')'>] (<','> inst)?
    obl-event = word [<'('> params <')'>]
    deadline = word [<'('> params <')'>]
    consequence = word [<'('> params <')'>]
    viol-event = word [<'('> params <')'>]
    viol = <'viol('> viol-event <'),'> inst
    inst = word
    end = <'\n'>* <'Passed(' number ')'> <'\n'>*
    params = word (<','> word)*
    <instant> = number
    <word> = #'[a-zA-Z\\-\\_\\']+'
    <words> = word (<' '> word)*
    <number> = #'[0-9]+'
"))


(defn solve-parse [text]
  (insta/add-line-and-column-info-to-metadata
   text
   (solver-parser text)))

(defn query-parse [text]
  (insta/add-line-and-column-info-to-metadata
   text
   (query-parser text)))

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


;; (-> (slurp "resources/output.txt")
;;     (solve-parse)
;;     (transform)
;;     (say-options)
;;     )

(defn parse-int [s]
  (Integer/parseInt (re-find #"\A-?\d+" s)))

(defn query-transform
  [ptree]
  (insta/transform
   {:instant (fn [& args] {:instant (parse-int (first args))})
    :inst (fn [& args] {:inst (first args)})
    :fluent (fn [& args] (apply merge (conj (rest args) {:fluent (first args)})))
    :perm (fn [& args] (apply merge (conj (rest args) {:perm (first args)})))
    :pow (fn [& args] {:pow (first args)})
    :consequence (fn [& args] {:consequence (apply merge (conj (rest args) {:event (first args)}))})
    :viol-event (fn [& args] (apply merge (conj (rest args) {:event (first args)})))
    :viol (fn [& args] {:viol (first args)})
    :deadline (fn [& args] {:deadline (apply merge (conj (rest args) {:event (first args)}))})
    :obl-event (fn [& args] (apply merge (conj (rest args) {:event (first args)})))
    :event (fn [& args] (apply merge (conj (rest args) {:event (first args)})))
    :live (fn [& args] {:live (first args)})
    :params (fn [& args] {:params args})
    :norm (partial merge)
    :obl (fn [& args] {:obl (apply merge args)})
    :observed (fn [& args] {:observed (apply merge args)})
    :occurred (fn [& args] {:occurred (apply merge args)})
    :holds (fn [& args] {:holds (apply merge args)})
    :step (fn [& args] args)
    :set-no (fn [& args] {:set (parse-int (first args))})
    :step-no (fn [& args] {:step (parse-int (first args))})
    :facts (fn [& args] {:facts args})
    :output (fn [& args]
              (let [stuff (apply concat (rest args))
                    facts (map :facts (get-if-key :facts stuff))
                    map-maker (fn [x] (hash-map
                                       :occurred (remove #(= (:event %) "null") (map :occurred (get-if-key :occurred x)))
                                       :observed (remove #(= (:event %) "null") (map :observed (get-if-key :observed x)))
                                       :viols (map :viol (get-if-key :viol x))
                                       :perms (into [] (get-if-key :perm (map :holds (get-if-key :holds x))))
                                       :obls (into [] (get-if-key :obl (map :holds (get-if-key :holds x))))
                                       :fluents (into [] (get-if-key :fluent (map :holds (get-if-key :holds x))))
                                       ;; :holds (map :holds (get-if-key :holds x))
                                       ))]
                (map map-maker facts)
                ;; args
                ;; facts
                ))}
   ptree))

(defn transform
  [ptree]
  (insta/transform
   {:instant (fn [& args] {:instant (parse-int (first args))})
    :inst (fn [& args] {:inst (first args)})
    :fluent (fn [& args] (apply merge (conj (rest args) {:fluent (first args)})))
    :perm (fn [& args] (apply merge (conj (rest args) {:perm (first args)})))
    :pow (fn [& args] {:pow (first args)})
    :viol (fn [& args] {:viol (first args)})
    :deadline (fn [& args] {:deadline (apply merge (conj (rest args) {:event (first args)}))})
    :obl-event (fn [& args] (apply merge (conj (rest args) {:event (first args)})))
    :event (fn [& args] (apply merge (conj (rest args) {:event (first args)})))
    :live (fn [& args] {:live (first args)})
    :params (fn [& args] {:params args})
    :norm (partial merge)
    :obl (fn [& args] {:obl (apply merge args)})
    :observed (fn [& args] (first args))
    :final (fn [& args] args)
    :output (fn [& args]
              (let [stuff (first args)] (hash-map
                            :perms (into [] (get-if-key :perm stuff))
                            :fluents (into [] (get-if-key :fluent stuff))
                            :events (into [] (get-if-key :event stuff))
                            :pows (into [] (get-if-key :pow stuff))
                            :obls (into [] (get-if-key :obl stuff)))))
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
                             :else (str (embellish (first (:params p))) " can " (:perm p) " " (embellish (second (:params p))) ".")
                             ))
        oblfn (fn [x] (let [o (:obl x)
                            ev (cond (nil? o) nil
                                     (= (count (:params o)) 1) (str (embellish (first (:params o))) " must " (embellish (:event o)))
                                     :else (str (embellish (first (:params o))) " must " (:event o) " " (embellish (second (:params o))))
                                     )]
                        (cond
                          (nil? ev) ev
                          (and (nil? (:viol o)) (nil? (:deadline o))) (str (embellish ev) ".")
                          (nil? (:viol o)) (str (embellish ev) " before " (embellish (first (:params (:deadline o)))) " " (:event (:deadline o)) " " (embellish (second (:params (:deadline o)))))
                          :else (str ev " before " (embellish (first (:params (:deadline o)))) " " (:event (:deadline o)) " " (embellish (second (:params (:deadline o)))) ", otherwise " (embellish (:viol o)) ".")
                          )))
        fluentfn (fn [f] (cond (nil? f) nil
                               (= (:fluent f) "null") nil
                               (nil? (:params f)) (str (embellish (:fluent f)) " is true.")
                               (= (count (:params f)) 1) (str (embellish (:fluent f)) " is " (embellish (first (:params f))))
                               :else (str (embellish (first (:params f))) "'s " (:fluent f) " is " (embellish (second (:params f))))
                               ))

        ;; p (println hmap)
        ;; now (last (sort (mapcat #(map :instant %) (vals hmap))))
        perms (map permfn (:perms hmap))
        ;; perms (map permfn (get-for-instant (:perms hmap) now))
        obls (map oblfn (:obls hmap))
        ;; obls (map oblfn (get-for-instant (:obls hmap) now))
        fluents (map fluentfn (:fluents hmap))
        ;; fluents (map fluentfn (get-for-instant (:fluents hmap) now))
        ]
    (reduce str (interpose "\n" (concat fluents perms obls)))
    ))

(defn occurred-prose [{:keys [inst params event viol]}]
  (let [policy (embellish inst)
        verb (embellish event)]
    (if viol
      (str "  VIOLATION: " (if (first (:params viol)) (embellish (first (:params viol)))) " " (embellish (:event viol)) (if (second (:params viol)) (str " " (embellish (second (:params viol)))) ".") (if (nth (:params viol) 2 nil) (str " " (embellish (nth (:params viol) 2)))) "\n")
      (str "  " (if (first params) (embellish (first params))) " " verb (if (second params) (str " " (embellish (second params))) ".") (if (nth params 2 nil) (str " " (embellish (nth params 2)))) "\n"))))

(defn legal-prose [{:keys [occurred viols]}]
  (str (apply str (map occurred-prose occurred))
       (if-not (empty? viols) (str "Violation:" (apply str (map occurred-prose viols)) "\n")))
  )

(defn legal-story [as]
  (str "The following occurred:\n" (apply str (interpose "Then:\n" (map legal-prose as)))))

(defn trace-to-prose [trace]
  (-> trace
      (solve-parse)
      (transform)
      (say-options)))

(defn answer-set-to-map [as]
  (-> as
      query-parse
      query-transform))

(defn answer-set-to-prose [as]
  (-> as
      query-parse
      query-transform
      legal-story))

(defn lawyer-talk [fname]
  (answer-set-to-prose (slurp fname)))

(defn explain [dir]
  (let [dir (clojure.java.io/file dir)
        files (file-seq dir)
        fnames (rest (map #(.getPath %) files))]
    (apply str (map-indexed (fn [i x] (str "---------------------------------------------------------------------\n\n" "Possibility " i ":\n\n" (lawyer-talk x) "\n")) fnames)
           ;; fnames
           )))

(defn trace-to-map [trace]
  (-> trace
      (solve-parse)
      (transform)))

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

;; (defn nlp-parse [text]
;;   (-> text
;;       (ark/tag)
;;       (make-ark-tree)
;;       (format-chars)))

;; (defn observe [text inst n]
;;   (let [ptree (nlp-parse text)
;;         hmap (apply hash-map (apply concat ptree))
;;         event (interpose "," (remove nil? [(:character hmap) (:object hmap)]))
;;         evf (if (empty? event) "" (reduce str (cons "," event)))
;;         ]
;;     ;; (str "observed(" (:verb hmap) "(player" evf ")," inst "," n ")")
;;     (str "observed(" (:verb hmap) "(lukeSkywalker" evf ")," inst")")
;;     ))

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
