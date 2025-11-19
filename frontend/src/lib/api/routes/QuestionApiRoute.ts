import { BaseApiRoute } from "$lib/api/routes/BaseApiRoute";
import type { QuestionCreate, QuestionUpdate } from "$lib/api/types/question";

export class QuestionApiRoute extends BaseApiRoute<QuestionCreate, QuestionUpdate> {
	constructor() {
		super("/api/questions");
	}
}
