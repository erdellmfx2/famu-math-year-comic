# Week Forty-Five: Tangent to Home

The full model took eleven minutes to produce an updated route recommendation.

The emergency-use target was under thirty seconds.

Keisha ran the benchmark again. Eleven minutes and four seconds.

"Consistency," Julian said, "is sometimes the enemy."

The Delta improvements had removed obvious inefficiencies. The remaining calculation examined too many interactions across the full network after every update.

Nia proposed a local approximation. Near the current conditions, a tangent-plane model could estimate how risk changed without rerunning everything.

Malik looked at the error plot.

"Approximation is how confident models lose when somebody finds the simplification," he said.

The room remembered his fall analytics competition, even if he did not name it yet.

## Friday, June 5: Eleven Minutes Late

Dr. Okafor asked what an emergency planner could do with a more exact answer delivered after traffic had already changed.

Malik defended the full model. It preserved interactions and avoided approximation error.

Keisha defended the benchmark. "It is too slow. That is not a minor implementation issue. Runtime changes whether the result can affect the decision."

Nia proposed using the full model for planning and precomputed scenarios, then a local linear approximation for rapid updates within a validated neighborhood of conditions.

The approximation would use partial derivatives to estimate how the output changed when warning delay, road capacity, and departure volume shifted slightly. It would fail if conditions moved too far from the expansion point or crossed a sudden discontinuity such as a road closure.

"Then we publish the interval and error bound," Nia said. "Outside it, the system reports that a full recalculation is required."

Malik heard the logic. Fear remained.

An eleven-minute answer felt irresponsible. A fast answer with visible error felt vulnerable to criticism. He had not yet separated those two threats.

## Saturday, June 6: The Judge in Malik's Head

Malik rebuilt the fall analytics loss in his memory.

His team had used an assumption that worked under ordinary scenarios. At regionals, judges found the hidden uncertainty. The model failed to advance. Malik had learned the wrong half of the lesson: any simplification could become the flaw that destroyed otherwise good work.

"You are arguing against approximation as a category," Nia told him. "Not this approximation."

"Because once people depend on the result, the error matters."

"Yes. That is why we measure it."

"And if conditions move outside the bound before the system detects it?"

"Then we design a trigger and test it."

Malik continued finding failure modes. Each one was legitimate. Together, they functioned as a refusal to choose any imperfect method.

Keisha interrupted. "The full model is also imperfect. Its error is arriving too late."

The sentence exposed the hidden comparison. Malik had treated exact computation as the safe baseline, though timing made it operationally unreliable.

He agreed to benchmark the local method.

Agreement did not make him comfortable.

## Sunday, June 7: Responsible in Time

Dr. Okafor compared two warnings.

One used the full model and arrived ten minutes after a road became unusable. The other used a bounded approximation and arrived in twenty seconds with a clearly displayed uncertainty range.

"Which is more responsible?" she asked.

"It depends on whether the approximation remains inside its validated region," Malik said.

"Good. Now answer under that condition."

He looked at the scenarios. "The approximation."

"Why?"

"Because decision value depends on timing as well as numerical accuracy."

They designed safeguards. The system monitored distance from the expansion point, changes in network topology, and estimated local error. If any threshold failed, it stopped presenting the approximation as current and requested a full model update.

The method would not be called exact. It would not be called safe under every condition. It would publish where it worked, where it did not, and how quickly that judgment could change.

Responsible mathematics was not the absence of approximation.

It was refusing to hide the terms under which an approximation deserved use.

## Monday, June 8: The Rooms Can Open

Celeste called Malik during lunch.

The final inspection had passed. The repaired back rooms could reopen if the family returned enough furniture over the weekend.

"Not everything," she said. "The large dresser may never come back. Your father says it can. Your father is wrong."

Marcel protested loudly in the background.

The family had stored furniture with relatives and in a rented unit. Moving it would require more hands than Marcel's recovering leg could safely provide.

Malik began building a schedule.

Then he paused.

"Would you be comfortable if some friends came to help?"

Celeste considered who he meant. "Friends, yes. Not a university service project. We are moving home, not becoming anybody's lesson."

"Understood."

Nia, Keisha, DJ, and Imani volunteered when Malik asked. They did not create matching shirts, social posts, or a fundraising caption.

They arranged rides and asked what tools to bring.

The rooms were ready for people.

That did not mean the house had returned to before.

## Tuesday, June 9: Come to Work, Not Rescue

The drive to Gulfport began before sunrise.

DJ controlled music until Keisha revoked his authority after three repeated songs. Imani brought breakfast. Nia carried work gloves and no prepared speech about resilience.

At the Baptiste home, Celeste assigned tasks within five minutes. DJ and Malik handled bed frames. Keisha labeled storage boxes. Imani organized kitchen items. Nia worked with Celeste to return books and photographs without blocking the hallway.

Marcel supervised more than he lifted, a limitation he disliked and respected after one warning look from his wife.

Twelve-year-old Micah appeared from a relative's house and appointed himself quality-control manager.

"That bed is crooked," he told DJ.

"The floor is expressive," DJ replied.

"The bed is crooked."

Micah was right.

No one framed the day as charity. The Baptistes fed everyone, gave orders, argued about furniture, and decided what returned. The friends supplied labor inside a family plan.

By evening, one bedroom held a made bed again.

Celeste stood in the doorway without calling the moment complete.

"Better," she said.

Better was enough for the day.

## Wednesday, June 10: The Line in the Closet

Nia carried a box of winter clothes into the back closet.

Inside, beneath fresh paint and above new baseboard, a faint waterline remained on an unfinished strip near the doorframe. The repair had covered most of the damage. Someone had chosen not to sand away this section yet.

Malik found her looking at it.

"My father wants to paint over it," he said. "My mother says we should photograph it first."

The line was not dramatic. It did not announce the months of repairs, the injury, insurance arguments, or uncertainty. It marked the height water had reached.

"This is why you hear uncertainty as danger," Nia said.

Malik nodded. "When people say a model is probably right, I see what happens in the probability they leave outside."

"And when I say approximation, you hear someone asking your family to accept the leftover risk."

"Yes."

Nia did not tell him the local method was safe. She understood why proof of bounded error mattered to him beyond academic rigor.

They photographed the line for Celeste, not for the project.

Then they returned to moving boxes.

Understanding did not require extraction.

## Thursday, June 11: Name the Fear in the Method

Back in Bellwether, the team completed the approximation benchmark.

Within the validated region, the local method produced updates in twelve seconds. Error stayed below the published threshold. When conditions approached a road closure or moved too far from the expansion point, the safeguard correctly stopped the estimate and requested full recalculation.

The result was not perfect.

It was usable under stated conditions.

At the design review, Malik supported the method.

"I resisted it because I feared hidden simplification," he said. "That fear comes from our fall analytics loss and from watching incomplete estimates shape my family's recovery. The fear identified real questions, but I used rigor as a way to avoid choosing any bounded uncertainty."

Nia described the local model. Keisha demonstrated the safeguard. The documentation listed runtime, error bounds, trigger conditions, and known failures.

Dr. Okafor approved the method for the next community-validation round.

Malik had not defeated fear by proving the approximation harmless. He had named the fear, tested its claims, and allowed the team to make a decision with visible limits.

The work moved forward.

So did the repaired rooms in Gulfport, holding new framing, old photographs, and one waterline the family had not yet decided whether to cover.
