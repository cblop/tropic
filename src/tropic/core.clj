(ns tropic.core
  (:require [tropic.parser :refer [transform parse]]))

(defn tropc
  [text]
  (transform (parse text) text))

(defn fix-crs [text]
  (clojure.string/replace text "\r" ""))

(defn -main
  [input output]
  (let [text (slurp input)
        result (tropc (fix-crs text))]
    (spit output result)))

