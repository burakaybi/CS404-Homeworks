

(define (problem CrossRiverBoat)

(:domain CrossingRiver)

(:objects
	fox goose beans farmer
    )

(:init

(onLeft fox)
(onLeft goose)
(onLeft beans)
(onLeft farmer)
				)

(:goal

(and
	(not(onLeft fox) )
	(not(onLeft goose))
	(not(onLeft beans))
	(not(onLeft farmer))
		)
	)
)


