(ns tropic.core-test
  (:require [clojure.test :refer :all]
            [instaparse.core :as insta]
            [tropic.core :refer :all]))

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

(tropical (multi [
                  "The Hero's journey is a trope"
                  "It begins when the Hero is at home"
                  "Then the hero gets a quest"
                  "It ends when the Hero returns"
                  ;;
                  "When the Hero gets a quest"
                  "The Hero must leave home"
                  "The Hero may sit"
                  "Finally, the Hero may destroy the Death Star"
                  ;;
                  "Destroy the Death Star is a task"
                  "To complete it, the Death Star must be destroyed"
                  "Otherwise, the rebel base explodes"
                  ;;
                  "The rebel base explodes is a consequence"
                  "If it happens, the Rebels die"
                  "If it happens, the Empire wins"
                  "Finally, the story ends"
                  ]))
(insta/visualize
 (tropical (multi [
                   "The Hero's journey is a trope"
                   "It begins when the Hero is at home"
                   "Then the hero gets a quest"
                   "It ends when the Hero returns"
                   ;;
                   "When the Hero gets a quest"
                   "The Hero must leave home"
                   "The Hero may sit"
                   "Finally, the Hero may destroy the Death Star"
                   ;;
                   "Destroy the Death Star is a task"
                   "To complete it, the Death Star must be destroyed"
                   "Otherwise, the rebel base explodes"
                   ;;
                   "The rebel base explodes is a consequence"
                   "If it happens, the Rebels die"
                   "If it happens, the Empire wins"
                   "Finally, the story ends"
                   ]))
 :output-file "resources/tree.png")

(tropical "Evil Empire is a trope")
(tropical "When the hero is at home")
(tropical "When the Wise Sage is in the dell")
(tropical "When Dan is in the Durley Dean")
(tropical "When Gandalf gets a quest")
(tropical "When the Wizard gets a quest\n")
(tropical "Destroy the Death Star is a task")


