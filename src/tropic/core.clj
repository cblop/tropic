(ns tropic.core
  (:require [tropic.parser :refer [transform parse]])
  (:gen-class))

(defn tropc
  [text]
  (transform (parse text) text))

(defn fix-crs [text]
  (clojure.string/replace text "\r" ""))

;; (defn -main
;;   [input output]
;;   (let [text (slurp input)
;;         result (tropc (fix-crs text))]
;;     (spit output result)))

(defn get-input []
  (do (println "Welcome to the land of adventure!")
      (print "> ")
      (loop [input (read-line) acc []]
        (if (= ":done" input)
          (println (reduce str (interpose ": yes!\n" acc)))
          (recur (read-line) (conj acc input))
          ))
    ))

(defn -main [& args]
  (get-input))

