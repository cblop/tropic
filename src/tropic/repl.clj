(ns tropic.repl
  (:require [tropic.solver :refer [make-story make-domain make-instal solve-story make-cmd trope-map st-map]]
            [tropic.gen :refer [make-map make-inst-map make-defs-map]]
            [tropic.parser :refer [parse-trope parse-defs parse-char parse-object parse-place trope-parser-fn]]
            [tropic.text-parser :refer [trace-to-prose trace-to-map query-transform lawyer-talk explain query-parse]]
            [tropic.instal :refer [instal instal-file external-events initially get-all-params generates]]))

(external-events {:characters [{:role "Hero", :label "Luke Skywalker", :id "586d153259111a0f09895659"} {:role "Villain", :label "Darth Vader", :id "586d153259111a0f0989565a"}], :objects [], :places [{:location "Away", :label "Space", :id "582487a35d2a0108a93fd8fa"} {:location "Home", :label "Tatooine", :id "582487a35d2a0108a93fd8fe"}], :subverted false, :events [{:role "Hero", :verb "go", :place "Home"} {:or [{:role "Hero", :verb "go", :place "Away"} {:role "Hero", :verb "kill", :role-b "Villain"}]}], :label "The Hero's Journey", :id "58806384a7986c11cd473ee5"})

(get-all-params {:characters [{:role "Hero", :label "Luke Skywalker", :id "586d153259111a0f09895659"} {:role "Villain", :label "Darth Vader", :id "586d153259111a0f0989565a"}], :objects [], :places [{:location "Away", :label "Space", :id "582487a35d2a0108a93fd8fa"} {:location "Home", :label "Tatooine", :id "582487a35d2a0108a93fd8fe"}], :subverted false, :events [{:role "Hero", :verb "go", :place "Home"} {:or [{:role "Hero", :verb "go", :place "Away"} {:role "Hero", :verb "kill", :role-b "Villain"}]}], :label "The Hero's Journey", :id "58806384a7986c11cd473ee5"})

(get-all-params {:label "The Hero's Journey", :events [{:or [{:role "The Hero", :verb "go", :place "Home"} {:role "Hero", :verb "go", :place "Home"} {:role "Mentor", :verb "go", :place "The Forest"} {:role "Villain", :verb "go", :place "Away"}]}], :situations []})

(generates {:label "The Hero's Journey", :events [{:or [{:role "The Hero", :verb "go", :place "Home"} {:role "Hero", :verb "go", :place "Home"} {:role "Mentor", :verb "go", :place "The Forest"} {:role "Villain", :verb "go", :place "Away"}]}], :situations []} [{:label "The Hero's Journey", :events [{:or [{:role "The Hero", :verb "go", :place "Home"} {:role "Hero", :verb "go", :place "Home"} {:role "Mentor", :verb "go", :place "The Forest"} {:role "Villain", :verb "go", :place "Away"}]}], :situations []}])
;; => {:label "The Hero's Journey", :events [{:or [{:role "The Hero", :verb "go", :place "Home"} {:role "Hero", :verb "go", :place "Home"} {:role "Mentor", :verb "go", :place "The Forest"} {:role "Villain", :verb "go", :place "Away"}]}], :situations []}

(initially {:story {:storyname "hj1", :tropes ("The Hero's Journey"), :instances ({:class "Hero", :iname "Luke Skywalker"} {:class "Villain", :iname "Darth Vader"} {:class "Mentor", :iname "Obi Wan"} {:class "Weapon", :iname "Light Saber"} {:class "Weapon", :iname "Sword"} {:class "Home", :iname "Tatooine"})}, :tropes ({:label "The Hero's Journey", :events [{:or [{:role "The Hero", :verb "go", :place "Home"} {:role "Hero", :verb "go", :place "Home"} {:role "Mentor", :verb "go", :place "The Forest"} {:role "Villain", :verb "go", :place "Away"}]}], :situations []}), :characters [{:role "Hero", :label "Luke Skywalker"} {:role "Villain", :label "Darth Vader"} {:role "Mentor", :label "Obi Wan"}], :objects [{:type "Weapon", :label "Light Saber"} {:type "Weapon", :label "Sword"}], :places [{:label "Tatooine", {:label "Space", :location "Away"} {:label "Alderaan", :location "The Forest"}, :location "Home"}], :player "Luke Skywalker"})
;; => {:story {:storyname "hj1", :tropes ("The Hero's Journey"), :instances ({:class "Hero", :iname "Luke Skywalker"} {:class "Villain", :iname "Darth Vader"} {:class "Mentor", :iname "Obi Wan"} {:class "Weapon", :iname "Light Saber"} {:class "Weapon", :iname "Sword"} {:class "Home", :iname "Tatooine"})}, :tropes ({:label "The Hero's Journey", :events [{:or [{:role "The Hero", :verb "go", :place "Home"} {:role "Hero", :verb "go", :place "Home"} {:role "Mentor", :verb "go", :place "The Forest"} {:role "Villain", :verb "go", :place "Away"}]}], :situations []}), :characters [{:role "Hero", :label "Luke Skywalker"} {:role "Villain", :label "Darth Vader"} {:role "Mentor", :label "Obi Wan"}], :objects [{:type "Weapon", :label "Light Saber"} {:type "Weapon", :label "Sword"}], :places [{:label "Tatooine", {:label "Space", :location "Away"} {:label "Alderaan", :location "The Forest"}, :location "Home"}], :player "Luke Skywalker"}


(defn join-strings [strs]
  (apply str (interpose "\n" strs)))

;; SUBLEASE ------------------------------------------------------
(def lease
  (join-strings
   ["\"Lease\" is a policy where:"
    "  The Lessor leases the Thing to the Lessee"
    "  The \"Maintenance of Confidence\" policy applies"]))


(parse-trope lease)
(make-map (parse-trope lease))

(def sublease
  (join-strings
   ["\"Sublease\" is a policy where:"
    "  The Lessor may sublease the Thing to a Third Party"]))


(parse-trope sublease)
;; it's because "permission" is in "events"
(make-map (parse-trope sublease))

(def sublease-permission
  (join-strings
   ["\"Sublease Permission\" is a policy where:"
    "  The Lessee may ask permission to sublease the Property"
    "  If the Lessor gives permission to the Lessee:"
    "    The \"Sublease\" policy applies"]))


(parse-trope sublease-permission)
(make-map (parse-trope sublease-permission))

(def maintenance-confidence
  (join-strings
   ["\"Maintenance of Confidence\" is a policy where:"
    "  The Lessee must pay the Lessor before the due date"
    "    Otherwise, the Lessor may cancel the contract"
    "  The Lessor must maintain the Thing"
    "    Otherwise, the Lessee may cancel the contract"]))


(parse-trope maintenance-confidence)
(make-map (parse-trope maintenance-confidence))

(def tenancy-agreement
  (join-strings
   ["\"Tenancy Agreement\" is a policy where:"
    "  The Lessor lets a Property"
    "  The \"Maintenance of Confidence\" policy applies"
    "  The Lessee must be quiet"
    "    Otherwise, the Lessor may cancel the contract"
    "  The Lessee must clean the Thing"
    "    Otherwise, the Lessor may cancel the contract"]))


(parse-trope tenancy-agreement)
(make-map (parse-trope tenancy-agreement))

;; WARRANTY ------------------------------------------------------

(def warranty
  (join-strings
   ["\"Warranty\" is a policy where:"
    "  The Buyer returns the Object"
    "  Then if the Object is defective:"
    "    The Seller must refund the Buyer"]))


(parse-trope warranty)
(make-map (parse-trope warranty))

(def warranty-release
  (join-strings
   ["\"Warranty Release\" is a policy where:"
    "  The \"Warranty\" policy does not apply"]))


;; not doing anything with "block" yet
(parse-trope warranty-release)
(make-map (parse-trope warranty-release))

(def est-rights
  (join-strings
   ["\"Establishment of Rights\" is a policy where:"
    "  The Seller gives Rights to a Third-Party"
    "  Then the \"Warranty Release\" policy does not apply"]))

(parse-trope est-rights)
(make-map (parse-trope est-rights))

(def sales-contract
  (join-strings
   ["\"Sales Contract\" is a policy where:"
    "  The Seller sells an Object to the Buyer"
    "  Then the \"Warranty\" policy applies"]))

(parse-trope sales-contract)
(make-map (parse-trope sales-contract))


(def charlist-policy
  [{:label "Alice" :role "Lessor"}
   {:label "Bob" :role "Lessee"}
   {:label "Charlotte" :role "Third party"}])


(def placelist-policy
  [])

(def objlist-policy
  [
   ;; {:label "Sales Rights" :type "Rights"}
   {:label "lawnmower" :type "Thing"}
   {:label "house" :type "Property"}])

(def pcd-one
  (join-strings
   ["\"pcd1\" is a policy where:"
    "  The Accessor may access Dataset1"
    "  Then the Accessor may access Dataset1"
    ]))

(def pcd-two
  (join-strings
   ["\"pcd2\" is a policy where:"
    "  The Accessor accesses Dataset2"
    "  Then the Accessor may not access Dataset2"]))

(def pcd-three
  (join-strings
   ["\"pcd3\" is a policy where:"
    "  The Accessor accesses Dataset1"
    "  Then the Accessor must contribute to Dataset2"]))


(def charlist-pcd
  [{:label "Alice" :role "Accessor"}
   {:label "d1" :role "Dataset1"}
   {:label "d2" :role "Dataset2"}])


(def placelist-pcd
  [])

(def objlist-pcd
  [])


(parse-trope pcd-one)
(parse-trope pcd-two)
(parse-trope pcd-three)
(st-map "pcd1" [pcd-one] charlist-pcd objlist-pcd placelist-pcd "Alice")
(st-map "hj1" [heros-journey] charlist objlist placelist "Luke Skywalker")


(test-story [pcd-three] charlist-pcd objlist-pcd placelist-pcd "Alice" "pcd3")
(solve-story "hj1" (map trope-map [heros-journey]) [(ev "go" "lukeSkywalker" "tatooine") (ev "go" "lukeSkywalker" "space")] 2)


(def heros-journey
  (join-strings
   ["\"The Hero's Journey\" is a trope where:"
    "  The Hero is at Home"
    ;; "    Then the Hero goes Away"
    "  Or the Hero goes Home"
    "  Or the Mentor goes to The Forest"
    "  Or the Villain goes Away"
    ]))

(def heros-journey
  (join-strings
   ["\"The Hero's Journey\" is a trope where:"
    "  The Hero is at Home"
    "  Then the Hero goes Away"
    "    Or the Villain kills the Hero"]))

(def heros-journey
  (join-strings
   ["\"The Hero's Journey\" is a trope where:"
    "  The Hero is at Home"
    "  Then the Hero goes Away"
    "  Then the Hero kills the Villain"]
   ))

(parse-trope heros-journey)
(trope-map (parse-trope heros-journey))
(trope-map heros-journey)

(def quest
  (join-strings
   ["The Quest is a trope where:"
    "  The Hero goes Away"
    "  Then the Hero returns Home"]))

(def evil-empire
  (join-strings
   ["\"The Evil Empire\" is a trope where:"
    "  The Villain has a Weapon"
    "  Then the Villain kills the Hero"]))

;; TESTS --------------


(def charlist
  [{:label "Luke Skywalker" :role "Hero"}
   {:label "Darth Vader" :role "Villain"}
   {:label "Obi Wan" :role "Mentor"}])


(def placelist
  [{:label "Tatooine" :location "Home"}
   {:label "Space" :location "Away"}
   {:label "Alderaan" :location "The Forest"}
   {:label "Japan" :location "Land of Adventure"}
   ])


(def objlist
  [{:label "Light Saber" :type "Weapon"}
   {:label "Sword" :type "Weapon"}])

;; PERMISSIONS------------------------------------------------------------

(def test-hj
  (join-strings
   ["\"The Heros Journey\" is a trope where:"
    "  The Hero is a role"
    "  The Villain is a role"
    "  Away is a place"
    "  Home is a place"
    "  The Hero goes Home"
    "  Then the Hero goes Away"]))

(parse-trope test-hj)
(trope-map test-hj)

(def test1
  (join-strings
   ["\"Test 1\" is a trope where:"
    "  The Hero is a role"
    "  The Land of Adventure is a place"
    "  The Home is a place"
    "  The Hero may go to the Land of Adventure"
    "  Then the Hero goes Home"
    ]))

(parse-trope test1)
(trope-map test1)
(st-map "test1" [test1] [test1] charlist objlist placelist "")
(:events (first (:tropes (st-map "test1" [test1] [test1] charlist objlist placelist ""))))
(test-story [test1] [test1] charlist objlist placelist "lukeSkywalker" "test1" 5)

(parse-defs test1)
(make-defs-map (parse-defs test1))
(parse-full-trope test1)
(:trope (make-defs-map (parse-defs test1)))
(trope-parser-fn (make-defs-map (parse-defs test1)))
;; (spit "resources/parser.txt" (trope-parser-fn (make-defs-map (parse-defs test1))))
(test-story [test1] charlist objlist placelist "lukeSkywalker" "test1" 5)

(def test2
  (join-strings
   ["\"Test 2\" is a trope where:"
    "  The Hero is a character"
    "  The Villain is a role"
    "  The Land of Adventure is a place"
    "  The Hero may go to the Land of Adventure"
    "  Then the Villain may kill the Hero"
    ]))

(parse-trope test2)
(trope-map test2)
(st-map "test2" [test2] charlist objlist placelist "")
(:events (first (:tropes (st-map "test2" [test2] charlist objlist placelist ""))))
(test-story [test2] charlist objlist placelist "lukeSkywalker" "test2" 5)

(parse-full-trope test2)
(parse-trope test2)
(st-map "test2" [test2] charlist objlist placelist "")
(test-story [test2] charlist objlist placelist "lukeSkywalker" "test2" 5)

(def test3
  (join-strings
   ["\"Test 3\" is a trope where:"
    "  The Hero is a role"
    "  The Villain is a role"
    "  The Land of Adventure is a place"
    "  The Hero may go to the Land of Adventure"
    "  Then the Villain may kill the Hero"
    "    Or the Villain may escape"
    ]))

(parse-trope test3)
(st-map "test3" [test3] charlist objlist placelist "")
(map :events (:tropes (st-map "test3" [test3] charlist objlist placelist "")))
(test-story [test3] charlist objlist placelist "lukeSkywalker" "test3" 5)

;; OBLIGATIONS -------------------------------------------------------------

(def test4
  (join-strings
   ["\"Test 4\" is a trope where:"
    "  The Hero is a role"
    "  The Land of Adventure is a place"
    "  The Hero must go to the Land of Adventure"
    ]))


(parse-trope test4)
(st-map "test4" [test4] charlist objlist placelist "")
(map :events (:tropes (st-map "test4" [test4] charlist objlist placelist "")))
(test-story [test4] charlist objlist placelist "lukeSkywalker" "test4" 5)

(def test5
  (join-strings
   ["\"Test 5\" is a trope where:"
    "  The Hero is a role"
    "  The Villain is a role"
    "  The Land of Adventure is a place"
    "  The Hero must go to the Land of Adventure"
    "    Otherwise, the Villain may kill the Hero"
    ]))

(parse-trope test5)
(st-map "test5" [test5] charlist objlist placelist "")
(map :events (:tropes (st-map "test5" [test5] charlist objlist placelist "")))
(test-story [test5] charlist objlist placelist "lukeSkywalker" "test5" 5)

(def test6
  (join-strings
   ["\"Test 6\" is a trope where:"
    "  The Hero is a role"
    "  The Villain is a role"
    "  The Mentor is a role"
    "  The Land of Adventure is a place"
    "  The Villain may kill the Mentor"
    "  The Hero must go to the Land of Adventure before the Villain kills the Mentor"
    ]))

(parse-trope test6)
(st-map "test6" [test6] charlist objlist placelist "")
(map :events (:tropes (st-map "test6" [test6] charlist objlist placelist "")))
(test-story [test6] charlist objlist placelist "lukeSkywalker" "test6" 5)

(def test7
  (join-strings
   ["\"Test 7\" is a trope where:"
    "  The Hero is a role"
    "  The Villain is a role"
    "  The Mentor is a role"
    "  The Land of Adventure is a place"
    "  The Hero must go to the Land of Adventure before the Villain kills the Mentor"
    "    Otherwise, the Villain may kill the Hero"
    ]))

(parse-trope test7)
(st-map "test7" [test7] charlist objlist placelist "")
(map :events (:tropes (st-map "test7" [test7] charlist objlist placelist "")))
(test-story [test7] charlist objlist placelist "lukeSkywalker" "test7" 5)

;; SEQUENCING ------------------------------------------------------------------------
(def test8
  (join-strings
   ["\"Test 8\" is a trope where:"
    "  The Hero is a role"
    "  The Villain is a role"
    "  Home is a place"
    "  The Land of Adventure is a place"
    "  The Hero may go to the Land of Adventure"
    "  Then the Hero may kill the Villain"
    "  Then the Hero may return Home"
    ]))

(parse-trope test8)
(st-map "test8" [test8] charlist objlist placelist "")
(map :events (:tropes (st-map "test8" [test8] charlist objlist placelist "")))
(test-story [test8] charlist objlist placelist "lukeSkywalker" "test8" 5)

;; BRANCHING --------------------------------------------------------------------------
(def test9
  (join-strings
   ["\"Test 9\" is a trope where:"
    "  The Hero is a role"
    "  The Villain is a role"
    "  The Land of Adventure is a place"
    "  The Hero may go to the Land of Adventure"
    "    Or the Hero may kill the Villain"
    ]))

(parse-trope test9)
(st-map "test9" [test9] charlist objlist placelist "")
(:events (first (:tropes (st-map "test9" [test9] charlist objlist placelist ""))))
(test-story [test9] charlist objlist placelist "lukeSkywalker" "test9" 5)

(def test10
  (join-strings
   ["\"Test 10\" is a trope where:"
    "  The Hero is a role"
    "  The Villain is a role"
    "  The Mentor is a role"
    "  The Land of Adventure is a place"
    "  Home is a place"
    "  The Hero may go to the Land of Adventure"
    "    Or the Hero may go Home"
    "    Or the Hero may kill the Villain"
    "    Or the Hero may visit the Mentor"
    ]))

(parse-trope test10)
(st-map "test10" [test10] charlist objlist placelist "")
(:events (first (:tropes (st-map "test10" [test10] charlist objlist placelist ""))))
(test-story [test10] charlist objlist placelist "lukeSkywalker" "test10" 5)


;; CONDITIONALS --------------------------------------------------------------------------------
(def test11
  (join-strings
   ["\"Test 11\" is a trope where:"
    "  The Hero is a role"
    "  The Villain is a role"
    "  The Land of Adventure is a place"
    "  The Hero may go to the Land of Adventure"
    "  Then the Hero may kill the Villain"
    "    If the Villain goes to the Land of Adventure"
    ]))

(parse-trope test11)
(st-map "test11" [test11] charlist objlist placelist "")
(:events (first (:tropes (st-map "test11" [test11] charlist objlist placelist ""))))
(test-story [test11] charlist objlist placelist "lukeSkywalker" "test11" 5)

(def test12
  (join-strings
   ["\"Test 12\" is a trope where:"
    "  The Hero is a role"
    "  The Villain is a role"
    "  The Land of Adventure is a place"
    "  Home is a place"
    "  The Hero may go to the Land of Adventure"
    "    If the Hero is at Home"
    "    If the Villain is at the Land of Adventure"
    ]))

(parse-trope test12)
(st-map "test12" [test12] charlist objlist placelist "")
(:events (first (:tropes (st-map "test12" [test12] charlist objlist placelist ""))))
(test-story [test12] charlist objlist placelist "lukeSkywalker" "test12" 5)

;; FLUENTS ---------------------------------------------------------------------------------------
(def test13
  (join-strings
   ["\"Test 13\" is a trope where:"
    "  The Hero is a role"
    "  Home is a place"
    "  The Hero is at Home"
    ]))

(parse-trope test13)
(st-map "test13" [test13] charlist objlist placelist "")
(:events (first (:tropes (st-map "test13" [test13] charlist objlist placelist ""))))
(test-story [test13] charlist objlist placelist "lukeSkywalker" "test13" 5)

(def test14
  (join-strings
   ["\"Test 14\" is a trope where:"
    "  The Hero is a role"
    "  The Villain is a role"
    "  The Land of Adventure is a place"
    "  Home is a place"
    "  The Villain is at the Land of Adventure"
    "  The Hero is at Home"
    ]))

(parse-trope test14)
(st-map "test14" [test14] charlist objlist placelist "")
(:events (first (:tropes (st-map "test14" [test14] charlist objlist placelist ""))))

(def test15
  (join-strings
   ["\"Test 15\" is a trope where:"
    "  The Hero is a role"
    "  The Villain is a role"
    "  The Land of Adventure is a place"
    "  Home is a place"
    "  The Hero is at Home"
    "  Then the Hero goes to the Land of Adventure"
    "  Then the Villain is at the Land of Adventure"
    ]))

(parse-trope test15)
(st-map "test15" [test15] charlist objlist placelist "")
(:events (first (:tropes (st-map "test15" [test15] charlist objlist placelist ""))))

(def test16
  (join-strings
   ["\"Test 16\" is a trope where:"
    "  The Hero is a role"
    "  The Villain is a role"
    "  The Land of Adventure is a place"
    "  The Weapon is an object"
    "  The Hero goes to the Land of Adventure"
    "  Then the Villain has a Weapon"
    ]))

(parse-trope test16)
(st-map "test16" [test16] charlist objlist placelist "")
(:events (first (:tropes (st-map "test16" [test16] charlist objlist placelist ""))))

;; EMBEDDING TROPES ------------------------------------------------------------------------------------
(def test17
  (join-strings
   ["\"Test 17\" is a trope where:"
    "  The Hero is a role"
    "  The Land of Adventure is a place"
    "  The Hero goes to the Land of Adventure"
    "  Then the \"Quest\" trope happens"
    ]))

(def test17a
  (join-strings
   ["\"Quest\" is a trope where:"
    "  The Hero is a role"
    "  The Land of Adventure is a place"
    "  Home is a place"
    "  The Hero goes to the Land of Adventure"
    "  Then the Hero goes Home"
    ]))

(parse-trope test17)
(st-map "test17" [test17] charlist objlist placelist "")
(:events (first (:tropes (st-map "test17" [test17] charlist objlist placelist ""))))
(test-story [test17a] charlist objlist placelist "lukeSkywalker" "test17a" 5)
(test-story [test17] charlist objlist placelist "lukeSkywalker" "test17" 5)
(test-story [test17 test17a] charlist objlist placelist "lukeSkywalker" "test17b" 5)

(def charlist
  [{:label "Luke Skywalker" :role "Hero"}
   {:label "Darth Vader" :role "Villain"}
   {:label "Obi Wan" :role "Mentor"}])


(def placelist
  [{:label "Tatooine" :location "Home"}
   {:label "Space" :location "Away"}
   {:label "Alderaan" :location "The Forest"}])


(def objlist
  [{:label "Light Saber" :type "Weapon"}
   {:label "Sword" :type "Weapon"}])

(def pcd-one
  (join-strings
   ["\"pcd1\" is a policy where:"
    "  The Accessor may access Dataset1"
    "  Then the Accessor may access Dataset1"
    ]))

(def pcd-one-a
  (join-strings
   ["\"pcd1\" is a policy where:"
    "  The Accessor may access Dataset1"
    "  Then the Accessor may access Dataset1"
    "  Then the Accessor may access Dataset1"
    ]))

(def pcd-two
  (join-strings
   ["\"pcd2\" is a policy where:"
    "  The Accessor may access Dataset2"
    "  Then the Accessor may not access Dataset2"
    ]))

(def pcd-three
  (join-strings
   ["\"pcd3\" is a policy where:"
    "  The Accessor may access Dataset1"
    "  Then the Accessor must contribute to Dataset2"
    ]))

(parse-trope pcd-one)
(parse-trope pcd-one-a)
(parse-trope pcd-two)
(parse-trope pcd-three)


(def charlist-pcd
  [{:label "Alice" :role "Accessor"}
   {:label "d1" :role "Dataset1"}
   {:label "d2" :role "Dataset2"}])


(def objlist-pcd
  [])

(def placelist-pcd
  [])

(st-map "pcd1" [pcd-one] charlist-pcd objlist-pcd placelist-pcd "Alice")
(test-story [pcd-one] charlist-pcd objlist-pcd placelist-pcd "Alice" "pcd1" 5)
(test-story [pcd-one-a] charlist-pcd objlist-pcd placelist-pcd "Alice" "pcd1" 5)


(defn ev
  ([verb player obj-a] {:verb verb :player player :object-a obj-a})
  ;; ([verb player obj-a obj-b] {:verb verb :player player :object-a obj-a :object-b obj-b})
  ([verb player obj-a obj-b] {:verb verb :player player :object-a obj-a :object-b obj-b}))


(defn test-story [ts ss chars objs places player out lookahead]
  (let [story-map (st-map out ts ss chars objs places player)]
    (make-story story-map out lookahead 100)))

(parse-trope heros-journey)
(st-map "hj1" [heros-journey] charlist objlist placelist "Luke Skywalker")
;; => {:story {:storyname "hj1", :tropes ("The Hero's Journey"), :instances ({:class "Hero", :iname "Luke Skywalker"} {:class "Villain", :iname "Darth Vader"} {:class "Mentor", :iname "Obi Wan"} {:class "Weapon", :iname "Light Saber"} {:class "Weapon", :iname "Sword"} {:class "Home", :iname "Tatooine"})}, :tropes ({:label "The Hero's Journey", :events [{:or [{:role "The Hero", :verb "go", :place "Home"} {:role "Hero", :verb "go", :place "Home"} {:role "Mentor", :verb "go", :place "The Forest"} {:role "Villain", :verb "go", :place "Away"}]}], :situations []}), :characters [{:role "Hero", :label "Luke Skywalker"} {:role "Villain", :label "Darth Vader"} {:role "Mentor", :label "Obi Wan"}], :objects [{:type "Weapon", :label "Light Saber"} {:type "Weapon", :label "Sword"}], :places [{:label "Tatooine", {:label "Space", :location "Away"} {:label "Alderaan", :location "The Forest"}, :location "Home"}], :player "Luke Skywalker"}
(trope-map heros-journey)
;; => {:label "The Hero's Journey", :events [{:or [{:role "The Hero", :verb "go", :place "Home"} {:role "Hero", :verb "go", :place "Home"} {:role "Mentor", :verb "go", :place "The Forest"} {:role "Villain", :verb "go", :place "Away"}]}], :situations []}

(ev "go" "Luke Skywalker" "tatooine")

;; TEST:
(test-story [heros-journey] charlist objlist placelist "Luke Skywalker" "hj1" 10)
(test-story [evil-empire] charlist objlist placelist "Luke Skywalker" "ee1" 10)
(test-story [heros-journey evil-empire] charlist objlist placelist "Luke Skywalker" "eehj1" 5)
(solve-story "hj1" (map trope-map [heros-journey]) [(ev "go" "lukeSkywalker" "tatooine") (ev "go" "lukeSkywalker" "space")] 3)
(solve-story "hj1" (map trope-map [heros-journey]) [(ev "go" "lukeSkywalker" "tatooine") (ev "go" "lukeSkywalker" "tatooine") (ev "go" "lukeSkywalker" "tatooine")] 2)
(solve-story "hj1" (map trope-map [heros-journey]) [(ev "go" "lukeSkywalker" "tatooine")] 3)
(solve-story "hj1" (map trope-map [heros-journey]) [] 5)
(solve-story "eehj1" (map trope-map [heros-journey evil-empire]) [] 10)
(solve-story "hj1" (map trope-map [heros-journey]) [(ev "go" "Luke Skywalker" "space")] 2)
;; (test-story [heros-journey quest] charlist objlist placelist "Luke Skywalker" "ex1")

;; (test-story [warranty warranty-release est-rights sales-contract] charlist-policy objlist-policy placelist-policy "Itsuki Hiroshi" "pol1")

;; (test-story [lease sublease] charlist-policy objlist-policy placelist-policy "Itsuki Hiroshi" "lease1")
;; (test-story [lease sublease sublease-permission maintenance-confidence tenancy-agreement] charlist-policy objlist-policy placelist-policy "Itsuki Hiroshi" "lease1")

(def events
  [(ev "lease" "Alice" "lawnmower")])
   ;; (ev "sublease")


(test-story [lease sublease sublease-permission maintenance-confidence tenancy-agreement] charlist-policy objlist-policy placelist-policy "Alice" "lease1")
(solve-story "lease1" (map trope-map [lease sublease sublease-permission maintenance-confidence tenancy-agreement]) nil)

;; (def parsed (:parsed (solve-story "lease1" (map trope-map [lease sublease sublease-permission maintenance-confidence tenancy-agreement]) nil)))
;; (spit "/tmp/parsed.txt" parsed)
;; (query-transform parsed)
(-> (slurp "resources/lease1/traces/trace-lease1-0.lp")
    query-parse
    query-transform
    )

;; (lawyer-talk "resources/lease1/trace-lease1-0.lp")
(spit "/tmp/explanation.txt" (explain "resources/lease1/traces"))

(do
  (solve-story "lease1" (map trope-map [lease sublease sublease-permission maintenance-confidence tenancy-agreement]) nil)
  (spit "resources/lease1/explanation.txt" (explain "resources/lease1/traces"))
  )

;; (trace-to-prose (:text (solve-story "lease1" (map trope-map [lease sublease sublease-permission maintenance-confidence tenancy-agreement]) (ev "leases" "Ituski Hiroshi" "Ishikawa Sayuri" "fune"))))
;; (spit "out.lp" (trace-to-prose (:text (solve-story "lease1" (map trope-map [lease sublease sublease-permission maintenance-confidence tenancy-agreement]) (ev "lease" "Ituski Hiroshi" "Ishikawa Sayuri" "fune")))))
;; (spit "/tmp/instal-error.txt" (solve-story "lease1" (map trope-map [lease sublease sublease-permission maintenance-confidence tenancy-agreement]) (ev "ride" "Ituski Hiroshi" "fune")))

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
