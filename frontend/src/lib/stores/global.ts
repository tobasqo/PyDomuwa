import type { GameCategory } from "$lib/api/types/game_category";
import type { GameType } from "$lib/api/types/game_type";
import type { QnACategory } from "$lib/api/types/qna_category";
import { readable } from "svelte/store";

export let gameTypesStore = readable<GameType[]>([]);
export let gameCategoriesStore = readable<GameCategory[]>([]);
export let qnaCategoriesStore = readable<QnACategory[]>([]);

export function initStores(
	gameTypes: GameType[],
	gameCategories: GameCategory[],
	qnaCategories: QnACategory[],
) {
	gameTypesStore = readable(gameTypes);
	gameCategoriesStore = readable(gameCategories);
	qnaCategoriesStore = readable(qnaCategories);
}
