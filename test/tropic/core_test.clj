(ns tropic.core-test
  (:require [clojure.test :refer :all]
            [instaparse.core :as insta]
            [tropic.core :refer :all]
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

(def sit-test
  (multi [
          "When the Hero gets a lightsaber"
          "The Hero must leave home if they have a spaceship"
          "The Hero may bring friends"
          "Finally, the Hero may destroy the Death Star"
          ]))

;; (instal (tropical test-string))
(tropical sit-test)

(html/select (tropical sit-test) [:situationdef])
(tropical test-string)

(def ptree (tropical test-string))

(:content (first (html/select ptree [:narrative :tropedef :trope])))
(html/select (html/select ptree [:narrative :tropedef]) [:event])
(html/select ptree [:tropedef])

(map get-trope (html/select ptree [:tropedef]))

(html/select ptree [:situationdef])

(get-taskdef (html/select ptree [:taskdef]))
(get-situation (html/select ptree [:situationdef]))
(get-deadline (html/select ptree [:situationdef]))
(get-consequence (html/select ptree [:situationdef]))
(get-sit-perms (html/select ptree [:situationdef]))
(get-sit-obls (html/select ptree [:situationdef]))
(get-perm (first (html/select ptree [:permission])))
(get-task (first (html/select ptree [:obligation])))
(get-cond (first (html/select ptree [:norms])))
(first (html/select ptree [:obligation]))

(situationdef-to-instal (get-situation (html/select ptree [:situationdef])))

(get-sit-perms ptree)

(map situationdef-to-instal (get-situations ptree))

(spit "resources/output.ial" (compile-instal ptree))

(reduce str (map tropedef-to-instal (get-tropes ptree)))
(spit "resources/output.ial" (reduce str (map tropedef-to-instal (get-tropes ptree))))

(tropical test-string)

(tropical (multi [
                  "The Hero's journey is a trope"
                  "It begins when the Hero is at home"
                  "Then the Hero gets a task"
                  "It ends when the Hero returns back home"
                  ;;
                  "When the Hero gets a lightsaber"
                  "The Hero must leave home"
                  "The Hero may bring friends"
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
                  ;;
                  "Star Wars is a story"
                  "It contains the Hero's Journey trope"
                  "It contains the Evil Empire trope"
                  "Luke Skywalker is its hero"
                  "Darth Vader is its villain"
                  "The end"
                  ]))
(insta/visualize
 (tropical (multi [
                  "The Hero's journey is a trope"
                  "It begins when the Hero is at home"
                  "Then the hero gets a task"
                  "It ends when the Hero returns"
                  ;;
                  "When the hero gets a lightsaber"
                  "The Hero must leave home"
                  "The Hero may bring friends"
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
                  ;;
                  "Star Wars is a story"
                  "It contains the Hero's Journey trope"
                  "It contains the Evil Empire trope"
                  "Luke Skywalker is its hero"
                  "Darth Vader is its villain"
                  "The end"
                   ]))
 :output-file "resources/tree.png")

(tropical "Evil Empire is a trope")
(tropical "When the hero is at home")
(tropical "When the Wise Sage is in the dell")
(tropical "When Dan is in the Durley Dean")
(tropical "When Gandalf gets a quest")
(tropical "When the Wizard gets a quest\n")
(tropical "Destroy the Death Star is a task")


