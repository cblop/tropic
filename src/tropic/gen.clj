(ns tropic.gen
  (:require [clojure.string :as str]
            [instaparse.core :as insta]))

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

(defn make-map [ptree]
  (insta/transform
   {:verb (partial param-map :verb)
    :item (partial param-map :object)
    :move (fn [& args] {:verb "go" :place (first (get-by-key :place args))})
    :mverb (partial param-map :mverb)
    :pverb (partial param-map :verb)
    :place (partial param-map :place)
    :character (partial param-map :role)
    :sequence (fn [& args] {:events (into [] (remove-blank args))})
    :situation (fn [& args] (first args))
    :situationdef (fn [& args] {:situation {:when (first args) :norms (into [] (map first (rest args)))}})
    :consequence (fn [& args] (hash-map :consequence (apply merge args)))
    :permission (fn [& args] (hash-map :permission (apply merge args)))
    :deadline (fn [& args] (hash-map :deadline (:consequence (first args))))
    :violation (fn [& args] (hash-map :violation (first (first args))))
    :visit (fn [& args] (hash-map :verb (first args) :place (:object (second args))))
    :give (fn [& args] (let [chars (get-by-key :role args)] {:verb "give" :from (first chars) :to (second chars) :object (first (get-by-key :object args))}))
    :meet (fn [& args] (let [chars (get-by-key :role args)] {:verb "meet" :role-a (first chars) :role-b (second chars)}))
    :kill (fn [& args] (let [chars (get-by-key :role args)] {:verb "kill" :role-a (first chars) :role-b (second chars)}))
    :task (partial merge)
    :norms (fn [& args] args)
    :obligation (fn [& args] {:obligation (apply merge args)})
    :event (partial merge)
    ;; :trope (fn [& args] {:trope {:roles (walk-get-key :role args)}})
    :trope (fn [& args] {:trope {:roles (vec (set (concat (walk-get-key :role (first args)) (walk-get-key :role-a (first args)) (walk-get-key :role-b (first args)))))
                                 :objects (vec (set (walk-get-key :object (first args))))
                                 :locations (vec (set (walk-get-key :place (first args))))
                                 :events (mapcat :events args)
                                 :situations (mapcat :situation args)}})
    }
   ptree))

