(define (domain CrossingRiver)
	(:requirements :adl :typing)
	(:types
		farmer fox goose beans
	)
	(:predicates (onLeft ?x))

(:action cross
		:parameters (?x)

:precondition 
(and
	(or 
		(and
			(onLeft ?x) 
			(onLeft farmer)
		)
			
		(and
			(not(onLeft ?x)) 
			(not(onLeft farmer))
		)
	)
	(or
		( = ?x goose)
		(and 
			(= ?x fox) 
			(or
				(and
					(onLeft goose)
					(not(onLeft beans))
				)
				(and
					(not(onLeft goose)) 
					(onLeft beans)
				)
			)
		)
		(and
			(= ?x beans)
			(or
				(and
					(onLeft fox)
					(not(onLeft goose))
				)
				(and
					(not(onLeft fox))
					(onLeft goose)
				)
			)
		)
		(and
			(= ?x farmer)
			(or
				(and
					(onLeft goose)
					(and
						(not(onLeft fox))
						(not(onLeft beans))
					)
				)
				(and
					(not(onLeft goose))
					(and
						(onLeft fox)
						(onLeft beans)
					)
				)
			)
		)
	)
)
:effect
(and
	(when (onLeft ?x)
		(and 
		(not (onLeft ?x))
		(not (onLeft farmer)))
	)
	(when (not (onLeft ?x))
		(and 
		(onLeft ?x)
		(onLeft farmer))
	)
)

)
)