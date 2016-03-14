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

(defn remove-blank [xs]
  (filter #(not (= (:verb %) "")) xs))

(defn make-map [ptree text]
  (insta/transform
   {:verb (partial param-map :verb)
    :item (partial param-map :object)
    :move (fn [& args] {:verb "go" :place (first (get-by-key :place args))})
    :mverb (partial param-map :mverb)
    :place (partial param-map :place)
    :character (partial param-map :role)
    :sequence (fn [& args] {:events (into [] (remove-blank args))})
    :trope (fn [& args] {:name (make-string args)})
    :roledef (partial apply hash-map)
    :situation (fn [& args] (first args))
    :situationdef (fn [& args] {:situation {:when (first args) :norms (into [] (map first (rest args)))}})
    ;; ;; :situation first
    :consequence (fn [& args] (hash-map :consequence (apply merge args)))
    ;; ;; :consequence (partial hash-map :consequence)
    :permission (fn [& args] (hash-map :permission (apply merge args)))
    :deadline (fn [& args] (hash-map :deadline (:consequence (first args))))
    :violation (fn [& args] (hash-map :violation (first (first args))))
    :visit (fn [& args] (hash-map :verb (first args) :place (:object (second args))))
    ;; :tropedef (fn [& args] {:trope (copy-meta (first args) (apply merge args))})
    :tropedef (fn [& args] {:trope {:name (first (get-by-key :name args))
                                    :situations (into [] (get-by-key :situation args))
                                    :events (apply concat (get-by-key :events args))}})
    :give (fn [& args] (let [chars (get-by-key :role args)] {:verb "give" :from (first chars) :to (second chars) :object (first (get-by-key :object args))}))
    :meet (fn [& args] (let [chars (get-by-key :role args)] {:verb "meet" :role-a (first chars) :role-b (second chars)}))
    :task (partial merge)
    ;; :norms (fn [& args] {:norms args})
    :norms (fn [& args] args)
    :obligation (fn [& args] {:obligation (apply merge args)})
    :event (partial merge)
    :class (fn [& args] {:class (make-string args)})
    :iname (fn [& args] {:iname (make-string args)})
    :instance (fn [& args] {:instance (apply merge args)})
    :storydef (fn [& args] {:storydef {:storyname (make-string (first (get-by-key :story args)))
                                       :tropes (map #(hash-map :name %) (get-by-key :name args))
                                       :instances (get-by-key :instance args)}})
    :story (fn [& args] {:story args})
    :quest (fn [& args] {:name (make-string args)})
    :questdef (fn [& args] {:quest {:name (first (get-by-key :name args))
                                    :norms (flatten (get-by-key :norms args))}})
    ;; :norms (fn [& args] {:norms (into [] args)})
    :narrative (fn [& args] (hash-map
                             :story (first (get-by-key :storydef args))
                             :tropes (into [] (get-by-key :trope args))
                             :quests (into [] (get-by-key :quest args))
                             :roles (into [] (get-by-key :role args))))
    }
   ptree))

