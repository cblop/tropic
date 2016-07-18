(ns tropic.repl
  (:require [tropic.solver :refer [make-story make-domain make-instal solve-story make-cmd]]
            [tropic.gen :refer [make-map make-inst-map]]
            [tropic.parser :refer [parse-trope parse-char parse-object parse-place]]
            [tropic.text-parser :refer [trace-to-prose trace-to-map]]
            [tropic.instal :refer [instal instal-file]]
            ))

(defn join-strings [strs]
  (apply str (interpose "\n" strs)))

(def heros-journey
  (join-strings
   ["The Hero is at Home"
    "Then the Quest happens"]))


(def quest
  {:label "The Quest"
   :string
   (join-strings
    ["The Hero goes Away"
     "Then the Hero returns Home"])})

(def evil-empire
  {:label "The Evil Empire"
   :string
   (join-strings
    ["The Villain has a Weapon"
     "The Villain may kill the Hero"])})

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

(defn trope-map [trope]
  {:label (:label (:trope trope))
   :events (:events (:trope (make-map (parse-trope (:string trope)))))
   :situations []}
  ;; also need: chars, obj, places?
  )

(defn st-map [name tropes chars objs places player]
  (let [trps (map trope-map tropes)
        role-pairs (map #(hash-map :class (:role %) :iname (:label %)) chars)
        obj-pairs (map #(hash-map :class (:type %) :iname (:label %)) objs)
        place-pairs (map #(hash-map :class (:location %) :iname (:label %)) places)
        story {:storyname name
               :tropes (map :label trps)
               :instances (concat role-pairs obj-pairs place-pairs)}
        ]
    {:story story
     :tropes trps
     :characters chars
     :objects objs
     :places places
     :player player
     }))

(defn ev
  ([verb player obj-a] {:verb verb :player player :object-a obj-a})
  ([verb player obj-a obj-b] {:verb verb :player player :object-a obj-a :object-b obj-b}))

;; TEST:
(make-story (st-map "test1" [heros-journey] charlist objlist placelist "Luke Skywalker") "test1")
(make-story (st-map "test1" [heros-journey evil-empire] charlist objlist placelist "Luke Skywalker") "test1")
(make-story (st-map "test2" [heros-journey quest] charlist objlist placelist "Luke Skywalker") "test2")
;; (:tropes (st-map "test2" [heros-journey quest] charlist objlist placelist "Luke Skywalker"))
(solve-story "test1" [heros-journey evil-empire] (ev "go" "Luke Skywalker" "tatooine"))
(:text (solve-story "test2" [heros-journey quest] (ev "go" "Luke Skywalker" "tatooine")))
(trace-to-map (:text (solve-story "test2" [heros-journey quest] (ev "go" "Luke Skywalker" "tatooine"))))
(spit "resources/result.txt" (trace-to-prose (:text (solve-story "test2" [heros-journey quest] (ev "go" "Luke Skywalker" "tatooine")))))
(spit "resources/result.txt" (trace-to-prose (:text (solve-story "test1" [heros-journey evil-empire] (ev "go" "Luke Skywalker" "tatooine")))))
(spit "resources/result.txt" (trace-to-prose (:text (solve-story "test1" [heros-journey evil-empire] (ev "has" "Darth Vader" "Sword")))))
(spit "resources/answer-set.lp" (solve-story "test2" [heros-journey quest] (ev "go" "Luke Skywalker" "tatooine")))
(solve-story "test1" [heros-journey evil-empire] (ev "go" "Luke Skywalker" "space"))

(parse-trope (:string heros-journey))
(make-map (parse-trope (:string heros-journey)))
(parse-trope (:string quest))

(parse-trope heros-journey-alt)
(make-map (parse-trope heros-journey-alt))

(parse-char "Luke Skywalker is a Hero")
(make-inst-map (parse-char "Luke Skywalker is a Hero"))
(parse-object "The Lightsaber is a Weapon")
(make-inst-map (parse-object "The Lightsaber is a Weapon"))
(parse-place "The beach is a resting place")
(make-inst-map (parse-place "The beach is a resting place"))

;; REMEMBER: initially takes hmap values from wrong place

;; (instal (st-map [heros-journey] charlist objlist placelist "Luke Skywalker"))
;; (make-instal (st-map [heros-journey] charlist objlist placelist "Luke Skywalker") "abc")

;; (parse-trope heros-journey)

;; (trope-map heros-journey)
;; (st-map [heros-journey] charlist objlist placelist "Luke Skywalker")

;; (make-map
;;  (parse-trope (:string heros-journey))
;;  )


