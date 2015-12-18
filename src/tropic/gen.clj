(ns tropic.gen
  (:require [clojure.string :as str]
            [com.rpl.specter :refer :all]
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

(defn make-map [ptree text]
  (insta/transform
   {:verb (partial param-map :predicate)
    :item (partial param-map :object)
    :place (partial param-map :object)
    :character (partial param-map :subject)
    :sequence (fn [& args] {:events (into [] args)})
    :trope (fn [& args] {:name (make-string args)})
    :situation (fn [& args] (first args))
    :situationdef (fn [& args] {:situation {:when (first args) :norms (into [] (map first (rest args)))}})
    ;; ;; :situation first
    :consequence (fn [& args] (hash-map :consequence (apply merge args)))
    ;; ;; :consequence (partial hash-map :consequence)
    :permission (fn [& args] (hash-map :permission (apply merge args)))
    :deadline (fn [& args] (hash-map :deadline (:consequence (first args))))
    :violation (partial hash-map :violation)
    :visit (fn [& args] (hash-map :predicate (first args) :object (:object (second args))))
    ;; :tropedef (fn [& args] {:trope (copy-meta (first args) (apply merge args))})
    :tropedef (fn [& args] {:trope {:name (first (get-by-key :name args))
                                    :situations (into [] (get-by-key :situation args))
                                    :events (first (get-by-key :events args))}})
    :task (partial merge)
    :obligation (fn [& args] {:obligation (apply merge args)})
    :event (partial merge)
    ;; :norms (fn [& args] {:norms (into [] args)})
    :norms (fn [& args] args)
    :narrative (fn [& args] (hash-map
                             :tropes (into [] (get-by-key :trope args))))
    }
   ptree))

