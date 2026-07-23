# Week Forty-Two: Lines That Do Not Meet

Dr. Okafor drew two lines in three-dimensional space.

They were not parallel. Their direction vectors pointed differently. Yet solving their parametric equations produced no shared point.

"Skew lines," Keisha said.

"Correct," Dr. Okafor replied. "Not parallel, not intersecting, and not contained in the same plane."

Nia looked at the board. In two dimensions, nonparallel lines eventually met. The extra dimension allowed them to pass without contact.

"So visual closeness can be misleading," Malik said.

"Frequently. Determine the geometry. Do not infer intersection from appearance."

Their summer roles occupied the same project. Their objectives, they would soon discover, did not yet meet.

## Friday, May 15: Passing in Different Planes

The class built equations for lines and planes from points and direction vectors.

Nia solved intersections by matching components. Malik used normal vectors to calculate distance from a point to a plane. Keisha found a computational method for determining whether two route segments crossed in three-dimensional space or only appeared to cross on a flat map.

That distinction mattered for overpasses, underpasses, and elevated roads. A two-dimensional network could mark two roads as connected when one passed above the other.

"That may explain three false route options," Keisha said.

They corrected the map topology before lunch.

The technical win put everyone in a generous mood. Malik used the opening to propose a new risk metric for the first summer design review.

"Minimize expected travel time across all modeled households," he said. "Include uncertainty penalties for unstable roads."

Nia read the equation. The average outcome improved.

Several neighborhoods with only one or two viable routes remained vulnerable.

"This does not protect people with the fewest choices," she said.

The generous mood left quietly.

## Saturday, May 16: Average Time or Minimum Access

Malik defended the expected-travel-time metric.

It reduced total exposure on the network. It could compare scenarios clearly. It avoided optimizing around rare edge cases at the expense of thousands of other travelers.

Nia objected to the phrase *edge cases*.

"The neighborhoods with one bridge or one elevated road are not errors at the edge of the data," she said. "They are the people most trapped by a bad recommendation."

She proposed an access metric that penalized scenarios leaving any neighborhood without a reliable route choice. Her approach protected the worst-served group, even if average travel time increased.

Malik pointed out that an extreme penalty could reroute large numbers of people inefficiently to improve one area's score by a small amount.

"And your average can look excellent while the same neighborhood loses every time," Nia replied.

Keisha listened from behind her laptop.

Both objectives were mathematically defensible. They optimized different outcomes.

Instead of recognizing the tradeoff, Malik and Nia each began treating the other metric as a disguised moral failure.

The first design review was scheduled for Sunday.

They carried the disagreement into it without translating first.

## Sunday, May 17: The Rejected Proposal Enters the Room

Dr. Okafor asked Nia to explain why her access penalty used the chosen threshold.

Nia cited the symposium model, community interviews, and the need to prevent route isolation.

Malik interrupted. "That threshold was designed for the fellowship presentation. We are supposed to validate the rejected proposal, not preserve it."

The word *rejected* changed the room.

Nia heard more than the technical criticism. She heard that her attachment to the project made her incapable of revising it, that the fellowship loss still defined her judgment, and that Malik had decided he was the person willing to say so.

"I am not preserving anything," she said. "I am protecting the exact households the judges said we had not represented."

"Then test whether the threshold does that. Do not keep it because it carries the values you presented."

"And do not remove it because averages are easier to price."

Dr. Okafor stopped the review.

"Your technical disagreement has become a trial of each other's motives," she said. "No useful design decision will come from that."

She ended the meeting without approving either metric.

The written boundaries had survived less than one week before pressure found their weakest seam.

## Monday, May 18: The People Missing From the Price

Nia arrived Monday still angry.

She reviewed Malik's metric and highlighted every place sparse data reduced estimated loss. Neighborhoods with fewer documented trips, lower insured property values, or inconsistent road records contributed less to the expected total.

"Your objective optimizes away the people whose data are hardest to price," she told him.

Malik went still.

The accusation struck his family history. Insurance records had captured repair materials more easily than displacement, lost work, or months of restricted rooms. Nia did not know that he had spent the weekend thinking about exactly those omissions.

"You think I do not understand missing loss because I use expected value?"

"I think the equation rewards whatever is easiest to count."

"Then criticize the equation. Do not assign me the values inside it."

Nia recognized too late that she had done what Dr. Okafor prohibited. Malik had challenged her threshold as preserved from rejection. She had answered by challenging his care for underdocumented people.

Neither had stayed inside the technical claim.

Keisha shut her laptop with a sound that ended the argument more effectively than shouting.

"Tomorrow," she said. "You are both bringing written work."

"What work?" Nia asked.

"Each other's."

## Tuesday, May 19: Write the Other Objective First

Keisha assigned the exercise at nine.

Malik had to write Nia's access objective accurately, including what it protected, where it could distort decisions, and what evidence would validate the threshold.

Nia had to write Malik's expected-travel-time objective with the same care.

They could not rebut anything until the other person approved the description.

Malik wrote that Nia's metric protected neighborhoods from route isolation and prevented aggregate improvement from hiding repeated harm. He identified its risk: an arbitrary threshold or extreme penalty could worsen systemwide evacuation without enough benefit.

Nia approved the description after changing *small neighborhoods* to *neighborhoods with fewer viable routes*.

Nia wrote that Malik's metric minimized total expected travel and exposure while accounting for uncertain capacity. It enabled scenario comparison and efficient use of the network. Its risk was that sparse or undervalued loss data could make severe local harm nearly invisible inside an average.

Malik approved it after she distinguished a flaw in the data from a flaw inherent to expected value.

Only then did Keisha allow discussion.

The room sounded different. They were no longer arguing over which person cared correctly. They were examining two objective functions with visible benefits and costs.

"We may need both," Malik said.

Nia nodded. "And we may need to show when they disagree."

## Wednesday, May 20: What the Standings Do Not Hold

Baseball's home finale honored seniors from a losing season.

The team was already eliminated from postseason contention. Still, the stands filled with families, alumni, and students. Senior posters lined the fence. A first baseman's little brother threw the ceremonial pitch several feet short of home and celebrated as if he had broken a record.

McCall-Hart lost the game in extra innings.

Afterward, seniors circled the field, thanked staff, and handed equipment to younger players. Julian's video featured the tutoring schedule, injury check-ins, and training standards they had created.

The standings measured wins and losses accurately.

They did not measure everything the seniors left behind.

Nia sat beside Malik with Keisha between them. No one used the game to solve the design review. But the evening gave their disagreement a useful frame: one metric could be valid and incomplete without becoming dishonest.

On the walk back, Malik said, "Expected time is still important."

"Yes," Nia replied. "So is minimum route access."

Keisha looked between them. "Amazing. Two days ago, that sentence required judicial intervention."

## Thursday, May 21: Show the Tradeoff

The revised model did not combine both objectives into one magical score.

Instead, it reported them side by side.

One panel showed expected travel time and total modeled exposure. Another showed the number of neighborhoods below the minimum access threshold and the severity of route isolation. A tradeoff curve displayed where improving one objective worsened the other.

Decision-makers could adjust weights, but the model recorded those choices rather than hiding them inside a default.

At the second design review, Malik explained the expected-value metric. Nia explained the access metric. Keisha demonstrated scenarios where they agreed and one where they strongly diverged.

"Which result do you recommend?" Dr. Okafor asked.

Malik answered first. "We cannot recommend a weight without community and agency input."

Nia continued, "Our result is that the tradeoff exists and becomes most severe where route data and options are sparse."

Dr. Okafor approved the design for community review.

Afterward, Nia apologized to Malik for assigning him the values of a flawed dataset. Malik apologized for turning her access threshold into evidence that she could not release the fellowship version.

The technical disagreement remained.

That was the point.

They had made it visible enough for evidence and community priorities to enter, rather than forcing one metric to pretend the conflict had disappeared.
