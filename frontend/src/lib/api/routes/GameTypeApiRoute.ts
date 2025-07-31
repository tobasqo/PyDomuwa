import { BaseApiRoute } from "$lib/api/routes/BaseApiRoute";
import type {
	GameType,
	GameTypeCreate,
	GameTypeUpdate,
} from "$lib/api/types/game_type";

export class GameTypeApiRoute extends BaseApiRoute<
	GameTypeCreate,
	GameTypeUpdate,
	GameType
> {
	constructor() {
		super("/api/game-types/");
	}
}
