# Week Forty-Four: The Gradient Trip

Dr. Okafor drew a surface representing storm risk.

Road capacity varied along one axis. Warning delay varied along another. Height represented modeled exposure.

She held warning delay fixed and changed road capacity. The resulting rate of change was one partial derivative.

Then she held capacity fixed and changed warning delay.

"Useful mathematics," she said. "Now tell me when holding one factor fixed becomes impossible."

Nia thought of traffic responding to warnings. Malik thought of insurance loss changing with both hazard and access. Keisha thought of software inputs that shared the same source.

In the real system, variables moved together.

Partial derivatives could isolate influence. They could not make isolation physically true.

## Friday, May 29: Hold One Thing Still

The class examined multivariable functions through tables, contour maps, and slices.

Nia used partial derivatives to test how sensitive route isolation was to one factor near a chosen scenario. Malik used them to examine expected loss. Keisha checked whether one input appeared in multiple transformations, making the assumption of independence suspect.

"A partial derivative answers a controlled question," Dr. Okafor said. "Do not report it as the whole system's response."

Before the Delta trip, the team created a dependency map. Warning delay affected departure volume. Departure volume affected congestion. Congestion affected travel time and route access. Changing one value while freezing the others could reveal local sensitivity, but the combined simulation had to restore the links.

They packed code, methods documents, consent limitations, and the rejected symposium poster.

"Do we need the poster?" Malik asked.

"It shows the version we are testing," Nia said.

"And what failed," Keisha added.

They rolled it into the travel tube.

Delta would receive the work with its history attached.

## Saturday, May 30: Orientation Before Access

The three-day Delta National Laboratory visit began with four hours of orientation.

Security staff checked identification and devices. An ethics officer explained acceptable data use. A governance specialist reviewed who could access each dataset, what transformations required documentation, and why downloading a convenient copy to a personal laptop could become a serious breach.

Only after lunch did the team see the supercomputing floor.

Keisha appreciated the order.

"Every brochure begins with the machines," she said. "The actual work begins with permissions."

Julian attended the communication track and learned which images could be recorded. Nia and Malik signed agreements acknowledging that lab data could not be blended with community interviews without review. Dr. Okafor made everyone describe the limits in their own words.

The computers were extraordinary. Rows of cabinets glowed behind glass while cooling systems moved heat away from thousands of processors.

None of that capacity granted the team authority to use every available record.

Power arrived after responsibility, not before it.

## Sunday, May 31: The Steepest Way Is Not the Safe Way

A Delta scientist projected a contour map of storm-surge height.

At one point, the gradient vector pointed in the direction of fastest increase. The negative gradient pointed toward fastest decrease.

"Would you evacuate exactly along the negative gradient?" she asked.

Several students said yes.

She added the road network.

The fastest decrease crossed marshland, a barrier, and an area without a drivable surface. Another direction reduced surge more slowly but followed an elevated road toward a shelter.

"Steepest improvement in one variable is not the safest feasible path," she said.

Nia saw their two-metric model again. Malik's expected-time objective and her access objective each defined a direction of improvement. Constraints and community knowledge determined which directions were possible and acceptable.

The scientist asked them to map the gradient of route risk. Keisha produced a local visualization. Malik identified where one small capacity change caused a large increase in expected exposure. Nia identified where the same change eliminated the only feasible route for one area.

The most important direction depended on what loss the team refused to hide.

## Monday, June 1: Fast Computer, Slow Model

Keisha ported a reduced model to Delta's test environment.

On the campus network, it handled a few thousand road segments. Delta supplied a much larger synthetic network with tens of thousands, denser intersections, and more scenario updates.

The model slowed to a crawl.

More computing power helped. It did not rescue an inefficient design.

The route-history system stored too much duplicate state. The access calculation recomputed neighborhoods unaffected by an update. Julian's visualization output was generated during simulation instead of afterward.

"Our model has reached the world's fastest environment and chosen embarrassment," Nia said.

Keisha did not laugh yet.

She profiled the code and displayed the bottlenecks. The team reduced redundant storage, separated simulation from media generation, and recalculated only affected regions. Runtime improved, then failed the emergency-response target anyway.

"Do not hide this from tomorrow's presentation," Dr. Okafor said.

Keisha added the failed benchmark to the first results slide.

The lab had not proven their model was powerful. It had made the weakness measurable.

## Tuesday, June 2: What Insurance Can See

Malik presented the risk assumptions to Delta scientists.

He showed expected travel time, modeled exposure, uncertainty penalties, and the gaps in insurance-derived loss data. He explained that documented property values could dominate records while displacement, unpaid caregiving, lost wages, and uninsured damage remained sparse.

A scientist asked whether adding a simple multiplier for underdocumented communities would correct the bias.

"It could acknowledge undercounting," Malik said, "but an unsupported multiplier may replace one false precision with another."

Another asked why the model used insurance data at all.

"Because it contains detailed, standardized records we do not have elsewhere. We need to use it without pretending documented financial loss equals total harm."

They challenged him to separate what the data measured, what proxies implied, and what the model could not price.

Malik revised the risk panel into three layers: documented loss, bounded proxy estimates, and unquantified impacts requiring narrative or community evidence.

The final category contained no convenient score.

Its emptiness was information.

## Wednesday, June 3: The People Outside the Vehicle Model

Nia presented the access metric.

She explained route isolation, minimum alternatives, warning delay, and motion updates. Then a transportation researcher asked how the model represented people without private vehicles.

It did not.

Nia could have pointed to future scope. Instead, she said the full sentence.

"Our current motion model begins after a private vehicle enters the road network. It cannot represent someone waiting for a bus, sharing a ride, walking to a pickup point, or depending on assisted transportation."

The omission affected every result. A neighborhood could appear to have road access while many residents had no way to enter the route.

The researcher recommended separating road availability from household mobility access. Nia added vehicle access, pickup delay, and transit capacity to the validation plan, but did not improvise values.

The presentation ended with fewer claims than it began.

Delta scientists praised the team's willingness to expose the gap and warned that honesty alone did not fix it.

Nia agreed.

## Thursday, June 4: The Terrace Without a Decision

The hotel terrace overlooked a parking lot and one determined tree growing through a crack near the wall.

After the final Delta session, Malik and Nia sat outside while the rest of the team packed.

"We said we would discuss fall after the work began," Nia said.

"We said no private promises before it began."

"That is not the same thing."

Malik agreed.

They spoke about Julian first. Nia explained that the relationship had been real, that public romance had hidden private disconnection, and that working together in spring felt safe because the relationship was over.

Malik spoke about Simone. He admitted that their relationship had been real too, and that he had compared it with an unfinished possibility often enough to make Simone feel partly unchosen.

"I was jealous of Julian before I had any right to be," he said.

"I was jealous of Simone while telling myself restraint made the feeling harmless," Nia replied.

They named the missed timing: fall, when Malik wanted Nia; spring, when Nia wanted Malik; summer, when both feelings existed but trust remained under construction.

"I do not want an answer tonight," Malik said.

"Neither do I."

The conversation brought them closer because it removed secrecy, not because it produced a decision.

They returned inside before the terrace could become another private world carrying more weight than the team.

The model still failed its runtime target. Malik's home still needed furniture moved. Closeness would have to live beside work that demanded action first.
