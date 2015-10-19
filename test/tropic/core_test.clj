(ns tropic.core-test
  (:require [clojure.test :refer :all]
            [tropic.core :refer :all]))

(deftest rules
  (testing "Testing rules"
    (testing "no parse errors"
      (is (vector? (inform "To exit: go north ")))
      (is (vector? (inform "Definition: a toad is ugly if warty.")))
      (is (vector? (inform "Definition: a toad is dying if its health is 10 or less")))
      (is (vector? (inform "To decide if the goblin is behind the door: go left")))
      (is (vector? (inform "This is the castle: inside lurks a goblin.")))
      )))

(inform "To exit: go north")
(inform "Definition: a toad is ugly if warty")
(inform "Definition: a toad is dying if its health is 10 or less")
(inform "To decide if the goblin is behind the door: go left")
