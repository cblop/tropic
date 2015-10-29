(ns tropic.core-test
  (:require [clojure.test :refer :all]
            [instaparse.core :as insta]
            [tropic.core :refer [tropc]]
            [tropic.parser :refer [parse transform]]
            [net.cgrand.enlive-html :as html]
            ))

(deftest rules
  (testing "Testing rules"
    (testing "no parse errors"
      (is (vector? (tropical "The Hero's Journey is a trope")))
      (is (vector? (tropical "Evil Empire is a trope.")))
      (is (vector? (tropical "When the hero is at home")))
      (is (vector? (tropical "When the Wise Sage is in the dell")))
      (is (vector? (tropical "When Dan is in the Durley Dean")))
      (is (vector? (tropical "When Gandalf gets a quest")))
      (is (vector? (tropical "Destroy the Death Star is a task")))
      )))

(defn multi [lines]
  (clojure.string/join "\n" lines))

(def test-string  (multi [
                          "The Hero's journey is a trope"
                          "It begins when the Hero is at home"
                          "Then the Hero gets a task"
                          "It ends when the Hero returns back home"
                          ;;
                          "The Evil Empire is a trope"
                          "It begins when the Empire does a bad thing"
                          "Then the Empire fights the hero"
                          "It ends when the Empire is defeated"
                          ;;
                          "When the Hero gets a lightsaber"
                          "The Hero must leave home before the Empire comes"
                          "Otherwise, the Empire kills the Hero"
                          "The Hero may bring friends"
                          "Finally, the Hero may destroy the Death Star"
                          ;;
                          "Destroy the Death Star is a task"
                          "To complete it, the Death Star must be destroyed"
                          "Otherwise, the Evil Empire destroys the rebel base"
                          ;;
                          "The rebel base explodes is a consequence"
                          "If it happens, the Rebels die"
                          "If it happens, the Empire wins"
                          "Finally, the story ends"
                          ;;
                          "Star Wars is a story"
                          "It contains the Hero's Journey trope"
                          "It contains the Evil Empire trope"
                          "Luke Skywalker is its hero"
                          "Darth Vader is its villain"
                          "The end"
                          ]))


(def trope-sit-test
  (multi [
          "The Hero's Journey is a trope where:"
          "  The Hero is at home"
          "  Then the Hero gets a task"
          "  Finally, the Hero returns home"
          "When the Hero gets a lightsaber:"
          "  The Hero must leave home before the Empire comes"
          "  Otherwise, the Empire kills the Hero"
          "  The Hero may bring friends"
          "  The Hero may destroy the Death Star"
          ]))

(parse trope-sit-test)
(transform (parse trope-sit-test) trope-sit-test)

(tropc trope-sit-test)

(spit "resources/output.ial" (tropc trope-sit-test))

