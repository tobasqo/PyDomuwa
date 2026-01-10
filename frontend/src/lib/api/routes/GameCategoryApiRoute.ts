import { BaseApiRoute } from "$lib/api/routes/BaseApiRoute";
import type {
  GameCategoryCreate,
  GameCategoryUpdate,
} from "$lib/api/types/game_category";

export class GameCategoryApiRoute extends BaseApiRoute<
  GameCategoryCreate,
  GameCategoryUpdate
> {
  constructor() {
    super("/api/game-categories/");
  }
}
