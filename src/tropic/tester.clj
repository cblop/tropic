(ns tropic.tester
  (:require [tropic.query :refer :all]
            [tropic.instal :refer [instal-file]]
            ))

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

(def test5 [
            "go(lukeSkywalker, tatooine)"
            "go(lukeSkywalker, space)"
            "meet(lukeSkywalker, obiWan)"
            ;; "gets(lukeSkywalker, lightsaber)"
            "go(lukeSkywalker, tatooine)"
            ])

(def test6 [
            "meet(lukeSkywalker, obiWan)"
            "gets(lukeSkywalker, lightsaber)"
            "go(lukeSkywalker, space)"
            "go(lukeSkywalker, tatooine)"
            ])

;; (def all-states (doall (map norms-at-state (range (count test1)))))

; Eval to test
(do
  (run-query test6 "test6")
  (let [all-states (doall (map norms-at-state (range (+ (count test6) 1))))]
    (spit "swout.edn" "")
    (doall (map #(spit "swout.edn" (prn-str %) :append true) all-states))))

(do
  (run-query test5 "test5")
  (let [all-states (doall (map norms-at-state (range (+ (count test5) 1))))]
    (spit "swout.edn" "")
    (doall (map #(spit "swout.edn" (prn-str %) :append true) all-states))))

(do
  (run-query test4 "test4")
  (let [all-states (doall (map norms-at-state (range (+ (count test4) 1))))]
    (spit "swout.edn" "")
    (doall (map #(spit "swout.edn" (prn-str %) :append true) all-states))))


(do
  (instal-file "resources/test1.story" "resources/test1.ial")
  (run-query test1 "test1")
  (let [all-states (doall (map norms-at-state (range (+ (count test1) 1))))]
    (spit "swout.edn" "")
    (doall (map #(spit "swout.edn" (prn-str %) :append true) all-states))))

(doall (map norms-at-state (range (count test5))))

;; (get-state 3)

(norms-at-state 0)
(norms-at-state 1)
(norms-at-state 2)
(norms-at-state 3)
(norms-at-state 4)
(norms-at-state 5)

(run-query test1)

(run-instal "test1")

(run-instal "test5")
(run-clingo "test5")
