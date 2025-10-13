import { BaseApiRoute } from "$lib/api/routes/BaseApiRoute";
import type { Question, QuestionCreate, QuestionUpdate } from "$lib/api/types/question";

export class QuestionApiRoute extends BaseApiRoute<
	QuestionCreate,
	QuestionUpdate,
	Question
> {
	constructor() {
		super("/api/questions");
	}
}
