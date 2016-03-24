(ns tropic.text-parser
  (:require [instaparse.core :as insta]
            [damionjunk.nlp.cmu-ark :as ark]
            [damionjunk.nlp.stanford :as stan]
            [clojure.string :as str]))

(def text-parser
  (insta/parser
   "input = verb <' '> <'at '>? <'to '>? <'the '>? object
    verb = 'look' | 'go' | 'take'
    object = word
    <word> = #'[0-9a-zA-Z\\-\\_\\']*'
    <words> = word (<' '> word)*"))

(def get-sentences (nlp/make-sentence-detector "models/en-sent.bin"))
(def tokenize (nlp/make-tokenizer "models/en-token.bin"))
(def pos-tag (nlp/make-pos-tagger "models/en-pos-maxent.bin"))
;; (def chunker (nlp/make-))

(defn parse
  [text]
  (insta/add-line-and-column-info-to-metadata
   text
   (text-parser text)))

(parse "look left")
(parse "look at the chair")
(parse "go to the cinema")
(parse "take the chair")

(defn make-ark-tree [tags]
  (into [] (remove nil? (map (fn [{:keys [token pos]}]
                               (cond (= pos "V") [:verb token]
                                     (= pos "N") [:object token]
                                     (= pos "^") [:character token]))
                             tags))))

(defn nlp-parse [text]
  (-> text
      (ark/tag)
      (make-ark-tree)))

(nlp-parse "give luke skywalker the lightsaber")
(ark/tag "talk to Luke Skywalker")


(ark/tag "look at the phone")
(make-tree (pos-tag (tokenize "go to the zoo")))
(make-tree (pos-tag (tokenize "throw the chair away")))
(make-tree (pos-tag (tokenize "go up")))
(make-tree (pos-tag (tokenize "look at the phone")))
(pos-tag (tokenize "go to the zoo"))
(pos-tag (tokenize "go north"))
(pos-tag (tokenize "look at the phone"))
(pos-tag (tokenize "examine the phone"))
