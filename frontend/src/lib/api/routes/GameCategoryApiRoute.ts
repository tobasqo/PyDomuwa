import { BaseApiRoute } from "$lib/api/routes/BaseApiRoute";
import type {
	GameCategory,
	GameCategoryCreate,
	GameCategoryUpdate,
} from "$lib/api/types/game_category";

export class GameCategoryApiRoute extends BaseApiRoute<
	GameCategoryCreate,
	GameCategoryUpdate,
	GameCategory
> {
	constructor() {
		super("/api/game-categories/");
	}
}
