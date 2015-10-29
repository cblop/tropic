(ns tropic.core
  (:require [tropic.parser :refer [transform parse]]))


(defn tropc
  [text]
  (transform (parse text) text))

