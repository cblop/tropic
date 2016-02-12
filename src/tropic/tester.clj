(ns tropic.tester
  (:require [tropic.query :refer :all]))

(def test1 [
            "go(lukeSkywalker, tatooine)"
            "meet(lukeSkywalker, obiWan)"
            "go(lukeSkywalker, space)"
            "go(lukeSkywalker, tatooine)"
            ])

(def test4 [
            "go(lukeSkywalker, tatooine)"
            "meet(lukeSkywalker, obiWan)"
            "gets(lukeSkywalker, lightsaber)"
            "bring(lukeSkywalker, hanSolo)"
            "go(lukeSkywalker, space)"
            "go(lukeSkywalker, tatooine)"
            ])

;; (def all-states (doall (map norms-at-state (range (count test1)))))

; Eval to test
(do
  (run-query test4)
  (let [all-states (doall (map norms-at-state (range (+ (count test4) 1))))]
    (spit "swout.edn" "")
    (doall (map #(spit "swout.edn" (prn-str %) :append true) all-states))))

(do
  (run-query test1)
  (let [all-states (doall (map norms-at-state (range (+ (count test1) 1))))]
    (spit "swout.edn" "")
    (doall (map #(spit "swout.edn" (prn-str %) :append true) all-states))))

(doall (map norms-at-state (range (count test1))))

(norms-at-state 0)
(norms-at-state 1)
(norms-at-state 2)
(norms-at-state 3)
(norms-at-state 4)
(norms-at-state 5)

(run-query test1)

(run-instal)
(run-clingo)
