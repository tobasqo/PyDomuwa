import { BaseApiRoute } from "$lib/api/routes/BaseApiRoute";
import type {
	QnACategory,
	QnACategoryCreate,
	QnACategoryUpdate,
} from "$lib/api/types/qna_category";

export class QnACategoryApiRoute extends BaseApiRoute<
	QnACategoryCreate,
	QnACategoryUpdate,
	QnACategory
> {
	constructor() {
		super("api/qna-categories/");
	}
}
