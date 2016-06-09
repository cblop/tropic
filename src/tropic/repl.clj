(ns tropic.repl
  (:require [tropic.solver :refer [make-story make-domain make-instal solve-story]]
            [tropic.gen :refer [make-map]]
            [tropic.parser :refer [parse-trope]]
            [tropic.instal :refer [instal instal-file]]
            ))

(defn join-strings [strs]
  (apply str (interpose "\n" strs)))

(def heros-journey
  {:label "The Hero's Journey"
   :string
   (join-strings
    ["The Hero is at Home"
     "Then the Hero goes Away"
     "Then the Hero returns Home"])})

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
  {:label (:label trope)
   :events (:events (:trope (make-map (parse-trope (:string trope)))))}
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
(solve-story "test1" (ev "go" "Luke Skywalker" "tatooine"))
(solve-story "test1" (ev "go" "Luke Skywalker" "space"))

;; (instal (st-map [heros-journey] charlist objlist placelist "Luke Skywalker"))
;; (make-instal (st-map [heros-journey] charlist objlist placelist "Luke Skywalker") "abc")

;; (parse-trope heros-journey)

;; (trope-map heros-journey)
;; (st-map [heros-journey] charlist objlist placelist "Luke Skywalker")

;; (make-map
;;  (parse-trope (:string heros-journey))
;;  )


