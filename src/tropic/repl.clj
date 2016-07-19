(ns tropic.repl
  (:require [tropic.solver :refer [make-story make-domain make-instal solve-story make-cmd trope-map st-map]]
            [tropic.gen :refer [make-map make-inst-map]]
            [tropic.parser :refer [parse-trope parse-char parse-object parse-place]]
            [tropic.text-parser :refer [trace-to-prose trace-to-map]]
            [tropic.instal :refer [instal instal-file]]
            ))

(defn join-strings [strs]
  (apply str (interpose "\n" strs)))

(def warranty
  (join-strings
   ["\"Warranty\" is a policy where:"
    "  The Buyer returns the Object"
    "  Then if the Object is defective:"
    "    The Seller must refund the Buyer"
    ]))

(parse-trope warranty)
(make-map (parse-trope warranty))

(def warranty-release
  (join-strings
   ["\"Warranty Release\" is a policy where:"
    "  The \"Warranty\" policy does not apply"
    ]))

;; not doing anything with "block" yet
(parse-trope warranty-release)
(make-map (parse-trope warranty-release))

(def est-rights
  (join-strings
   ["\"Establishment of Rights\" is a policy where:"
    "  The Seller gives Rights to a Third-Party"
    "  Then the \"Warranty Release\" policy does not apply"]))

(parse-trope est-rights)
;; not picking up roles for some reason
(make-map (parse-trope est-rights))

(def sales-contract
  (join-strings
   ["\"Sales Contract\" is a policy where:"
    "  The Seller sells an Object to the Buyer"
    "  Then the \"Warranty\" policy applies"]))

(parse-trope sales-contract)
(make-map (parse-trope sales-contract))


(def charlist-policy
  [{:label "Itsuki Hiroshi" :role "Seller"}
   {:label "Ishikawa Sayuri" :role "Buyer"}
   {:label "Kitajima Saburo" :role "Third party"}
   ])

(def placelist-policy
  [])

(def objlist-policy
  [{:label "Sales Rights" :type "Rights"}
   {:label "Ukai-bune" :type "Object"}
   ])


(def heros-journey
  (join-strings
   ["The Hero's Journey is a trope where:"
    "  The Hero is at Home"
    "  Then the Quest happens"]))

(def quest
  (join-strings
   ["The Quest is a trope where:"
    "  The Hero goes Away"
    "  Then the Hero returns Home"]))

(def evil-empire
  (join-strings
   ["The Evil Empire is a trope where:"
    "  The Villain has a Weapon"
    "  The Villain may kill the Hero"]))

(def charlist
  [{:label "Luke Skywalker" :role "Hero"}
   {:label "Darth Vader" :role "Villain"}
   ])

(def placelist
  [{:label "Tatooine" :location "Home"}
   {:label "Space" :location "Away"}
   ])

(def objlist
  [{:label "Light Saber" :type "Weapon"}
   {:label "Sword" :type "Weapon"}
   ])


(defn ev
  ([verb player obj-a] {:verb verb :player player :object-a obj-a})
  ([verb player obj-a obj-b] {:verb verb :player player :object-a obj-a :object-b obj-b}))

(defn test-story [ts chars objs places player out]
  (let [story-map (st-map out ts chars objs places player)]
    (make-story story-map out)))

;; TEST:
(test-story [heros-journey quest] charlist objlist placelist "Luke Skywalker" "ex1")

(test-story [warranty warranty-release est-rights sales-contract] charlist-policy objlist-policy placelist-policy "Itsuki Hiroshi" "pol1")

;; TEST:
;; (make-story (st-map "test1" [heros-journey] charlist objlist placelist "Luke Skywalker") "test1")
;; (make-story (st-map "test1" [heros-journey evil-empire] charlist objlist placelist "Luke Skywalker") "test1")
;; (make-story (st-map "test2" [heros-journey quest] charlist objlist placelist "Luke Skywalker") "test2")
;; ;; (:tropes (st-map "test2" [heros-journey quest] charlist objlist placelist "Luke Skywalker"))
;; (solve-story "test1" [heros-journey evil-empire] (ev "go" "Luke Skywalker" "tatooine"))
;; (:text (solve-story "test2" [heros-journey quest] (ev "go" "Luke Skywalker" "tatooine")))
;; (trace-to-map (:text (solve-story "test2" [heros-journey quest] (ev "go" "Luke Skywalker" "tatooine"))))
;; (spit "resources/result.txt" (trace-to-prose (:text (solve-story "test2" [heros-journey quest] (ev "go" "Luke Skywalker" "tatooine")))))
;; (spit "resources/result.txt" (trace-to-prose (:text (solve-story "test1" [heros-journey evil-empire] (ev "go" "Luke Skywalker" "tatooine")))))
;; (spit "resources/result.txt" (trace-to-prose (:text (solve-story "test1" [heros-journey evil-empire] (ev "has" "Darth Vader" "Sword")))))
;; (spit "resources/answer-set.lp" (solve-story "test2" [heros-journey quest] (ev "go" "Luke Skywalker" "tatooine")))
;; (solve-story "test1" [heros-journey evil-empire] (ev "go" "Luke Skywalker" "space"))

;; (parse-trope (:string heros-journey))
;; (parse-trope heros-journey)
;; (make-map (parse-trope (:string heros-journey)))
;; (parse-trope (:string quest))

;; (parse-trope heros-journey-alt)
;; (make-map (parse-trope heros-journey-alt))

;; (parse-char "Luke Skywalker is a Hero")
;; (make-inst-map (parse-char "Luke Skywalker is a Hero"))
;; (parse-object "The Lightsaber is a Weapon")
;; (make-inst-map (parse-object "The Lightsaber is a Weapon"))
;; (parse-place "The beach is a resting place")
;; (make-inst-map (parse-place "The beach is a resting place"))

;; ;; REMEMBER: initially takes hmap values from wrong place

;; ;; (instal (st-map [heros-journey] charlist objlist placelist "Luke Skywalker"))
;; ;; (make-instal (st-map [heros-journey] charlist objlist placelist "Luke Skywalker") "abc")

;; ;; (parse-trope heros-journey)

;; ;; (trope-map heros-journey)
;; ;; (st-map [heros-journey] charlist objlist placelist "Luke Skywalker")

;; ;; (make-map
;; ;;  (parse-trope (:string heros-journey))
;; ;;  )


