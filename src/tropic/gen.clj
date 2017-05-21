(ns tropic.gen
  (:require [clojure.string :as str]
            [clj-wordnet.core :refer [make-dictionary]]
            [instaparse.core :as insta]))

(def wordnet (make-dictionary "dict/"))

(defn convert-verb [word]
  (:lemma (first (wordnet word :verb))))

(defn camel-case [verb]
  )

(defn copy-meta
  [old new]
  (with-meta new (meta old)))

(defn make-string [words]
  (reduce str (interpose " " words)))

(defn param-map [key & args]
  (hash-map key (make-string args)))

(defn get-by-key [key xs]
  (map #(get % key) (filter #(get % key) xs)))

(defn walk-get-key [key xs]
  (->> (tree-seq #(or (map? %) (vector? %)) identity xs)
       (filter #(if (and (map? %) (get % key)) true false))
       (map #(str/capitalize (get % key)))
       set
       vec))

(defn remove-blank [xs]
  (filter #(not (= (:verb %) "")) xs))

(defn process-ifs [events]
  (loop [evs events acc [] ifs []]
    (if (empty? evs) acc
        (cond
          (and (not (:if (first evs))) (:if (second evs))) (recur (rest evs) acc (conj ifs (first evs)))
          (and (:if (first evs)) (:if (second evs))) (recur (rest evs) acc (conj ifs (:if (first evs))))
          (and (:if (first evs)) (not (:if (second evs)))) (recur (rest evs) (conj acc {:if (conj ifs (:if (first evs)))}) [])
          :else (recur (rest evs) (conj acc (first evs)) ifs)
          )
        )))

(defn process-ors [events]
  (loop [evs events acc [] ors []]
    (if (empty? evs) acc
        (cond
          (and (not (:or (first evs))) (:or (second evs))) (recur (rest evs) acc (conj ors (first evs)))
          (and (:or (first evs)) (:or (second evs))) (recur (rest evs) acc (conj ors (:or (first evs))))
          (and (:or (first evs)) (not (:or (second evs)))) (recur (rest evs) (conj acc {:or (conj ors (:or (first evs)))}) [])
          :else (recur (rest evs) (conj acc (first evs)) ors)
          )
        )))

;; (process-ors (:events {:label "The Hero's Journey", :events '({:role "The Hero", :verb "go", :place "Home"} {:role "Hero", :verb "go", :place "Away"} {:or {:role "Hero", :verb "go", :place "Home"}} {:or {:role "Villain", :verb "go", :place "Away"}}), :situations []}))

(defn make-defs-map [ptree]
  (insta/transform
   {
    :label (fn [& args] {:label (make-string args)})
    :chardef (fn [& args] {:chardef (make-string args)})
    :objdef (fn [& args] {:objdef (make-string args)})
    :placedef (fn [& args] {:placedef (make-string args)})
    :trope (fn [& args] {:trope (str "  " (apply str (interpose "\n  " args)))})
    :text (fn [& args] {
                        :label (first (filter some? (map :label args)))
                        :roles (filter some? (map :chardef args))
                        :objects (filter some? (map :objdef args))
                        :places (filter some? (map :placedef args))
                        :trope (first (filter some? (map :trope args)))
                        })
    }
   ptree))

(defn make-map [ptree]
  (insta/transform
   {
    :character (partial param-map :role)
    :verb (fn [& args] {:verb (convert-verb (apply str (interpose " " args)))})
    :permission (fn [& args] (let [chars (get-by-key :role args)] (merge
                                                                   (dissoc (apply merge args) :role)
                                                             (if (> (count chars) 1)
                                                               {:role-a (first chars)
                                                                :role-b (second chars)})
                                                             (if (= (count chars) 1)
                                                               {:role (first chars)})
                                                             )))

    :action (fn [& args] (let [chars (get-by-key :role args)] (merge
                                                              (dissoc (apply merge args) :role)
                                                              (if (> (count chars) 1)
                                                                {:role-a (first chars)
                                                                 :role-b (second chars)})
                                                              (if (= (count chars) 1)
                                                                {:role (first chars)})
                                                              )))
    :event (fn [& args] (let [chars (get-by-key :role args)] (merge
                                                                   (dissoc (apply merge args) :role)
                                                                   (if (> (count chars) 1)
                                                                     {:role-a (first chars)
                                                                      :role-b (second chars)})
                                                                   (if (= (count chars) 1)
                                                                     {:role (first chars)})
                                                                   )))
    :item (partial param-map :object)
    :fverb (fn [& args] {:verb (first args)})
    :place (partial param-map :place)
    :conditional (fn [& args] {:if (apply merge args)})
    :outcome (fn [& args] {:then (first args)})
    :adjective (partial param-map :adjective)
    ;; :whitespace (fn [& args] :whitespace)
    :object (partial param-map :object)
    :fluent (partial merge)
    :sequence (fn [& args] {:events (into [] (remove-blank args))})
    :or (partial param-map :or)
    :if (partial param-map :if)
    :consequence (fn [& args] (hash-map :consequence (apply merge args)))
    :rempermission (fn [& args] (hash-map :rempermission (apply merge args)))
    :deadline (fn [& args] (hash-map :deadline (:consequence (first args))))
    :violation (fn [& args] (hash-map :violation (first (first args))))
    :task (partial merge)
    :norms (fn [& args] (first args))
    :obligation (fn [& args] {:obligation (apply merge args)})
    ;; :event (partial merge)
    ;; :action (partial merge)
    :happens (partial merge)
    :block (fn [& args] {:block (:subtrope (first args))})
    ;; :trope (fn [& args] {:trope {:roles (walk-get-key :role args)}})
    :subtrope (fn [& args] {:subtrope (make-string args)})
    :label (fn [& args] {:label (make-string args)})
    :trope (fn [& args] {:trope {:label (first (filter some? (map :label args)))
                                 :roles (vec (set (concat (mapcat #(walk-get-key :role %) args) (mapcat #(walk-get-key :role-a %) args) (mapcat #(walk-get-key :role-b %) args))))
                                 :objects (vec (set (mapcat #(walk-get-key :object %) args)))
                                 :locations (vec (set (mapcat #(walk-get-key :place %) args)))
                                 :events (process-ifs (process-ors (mapcat :events args)))
                                 ;; :events (mapcat :events args)
                                 :situations (mapcat :situation args)}})
    }
   ptree))

(defn make-inst-map [ptree]
  (insta/transform
   {:role (fn [& args] {:role (make-string args)})
    :type (fn [& args] {:type (make-string args)})
    :location (fn [& args] {:location (make-string args)})
    :label (fn [& args] {:label (make-string args)})
    :character (fn [& args] {:label (first (filter some? (map :label args)))
                          :role (first (filter some? (map :role args)))})
    :object (fn [& args] {:label (first (filter some? (map :label args)))
                          :type (first (filter some? (map :type args)))})
    :place (fn [& args] {:label (first (filter some? (map :label args)))
                          :location (first (filter some? (map :location args)))})
    }
   ptree))

