import { BaseApiRoute } from "$lib/api/routes/BaseApiRoute";
import type { QnACategoryCreate, QnACategoryUpdate } from "$lib/api/types/qna_category";

export class QnACategoryApiRoute extends BaseApiRoute<
  QnACategoryCreate,
  QnACategoryUpdate
> {
  constructor() {
    super("/api/qna-categories/");
  }
}
