(ns tropic.core-test
  (:require [clojure.test :refer :all]
            [instaparse.core :as insta]
            [tropic.core :refer [tropc -main]]
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
          ;; "A Hero is a type of Character"
          ;; "A Villain is a type of Character"
          "\"The Hero's Journey\" is a trope where:"
          "  The Hero is at home"
          "  Then the Hero gets a task"
          "  Then the Hero returns home"
          "\"The Evil Empire\" is a trope where:"
          "  The Villain does a bad thing"
          "  Then the Villain fights the hero"
          "  Then the Villain is defeated"
          "When the Hero gets a lightsaber:"
          "  The Hero must leave home before the Villain comes"
          "    Otherwise, the Villain kills the Hero"
          "  The Hero may bring friends"
          "  The Hero may destroy the Death Star"
          "When the Villain gets a hostage:"
          "  The Villain may destroy Alderaan"
          ]))

(def character-test
  (multi [
          "A hero is a type of character who:"
          "  Cannot kill someone"
          "A villain is a type of character who:"
          "  Can kill someone"
          ]))

(parse character-test)

(parse (str character-test "\n" slapstick-test))

(def story-test
  (multi [
          "\"Punch and Judy\" is a story:"
          "  It contains the \"Villain protagonist\" trope"
          "  It contains the \"Slapstick\" trope"
          "  It contains the \"Karma Houdini\" trope"
          "  Its scenes are:"
          "    \"Sausages\""
          "    Then \"Punch kills the baby\""
          "  Punch is its hero"
          "  Joey is its dispatcher"
          "  Snap is its rogue"
          ]))

(parse story-test)

(def scene-test
  (multi [
          "\"Sausages\" is a scene:"
          "  It contains the \"Don't touch it\" trope"
          "  Starring Punch, Judy, Snap and Joey"
          "  It has sausages"
          ]))

(parse scene-test)

(def slapstick-test
  (multi [
          "\"Slapstick\" is a trope where:"
          "  The hero is also the villain"
          "  The audience may laugh"
          "  The hero falls over"
          "    Or the villain slips up"
          "  When someone hits someone else:"
          "    The audience will laugh"
          ]))

(parse slapstick-test)

(def touch-test
  (multi [
          "\"Don't touch it\" is a trope where:"
          "  The dispatcher leaves an object"
          "  Then the dispatcher leaves"
          "  Then the rogue takes the object"
          ;; "    Or the hero breaks the object"
          ;; "  Then the dispatcher returns"
          ]))

(parse touch-test)
(tropc touch-test)

(parse trope-sit-test)
(transform (parse trope-sit-test) trope-sit-test)

(tropc trope-sit-test)
(spit "resources/output.ial" (tropc trope-sit-test))

(-main "resources/starwars.story" "resources/output.ial")

(def role-test
  (multi [
          "A Hero is a type of Character"
          "A Villain is a type of Character"
          "A Hero can:"
          "  Visit the Death Star"
          ]))

(parse role-test)
(tropc role-test)

(tropc trope-sit-test)

(spit "resources/output.ial" (tropc trope-sit-test))

