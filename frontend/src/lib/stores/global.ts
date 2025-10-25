import type { GameCategory } from "$lib/api/types/game_category";
import type { GameType } from "$lib/api/types/game_type";
import type { QnACategory } from "$lib/api/types/qna_category";
import { writable, type Readable } from "svelte/store";

const { subscribe: subscribeGameTypes, set: setGameTypes } = writable<GameType[]>([]);
const { subscribe: subscribeGameCategories, set: setGameCategories } = writable<
	GameCategory[]
>([]);
const { subscribe: subscribeQnaCategories, set: setQnaCategories } = writable<
	QnACategory[]
>([]);

export const gameTypesStore: Readable<GameType[]> = { subscribe: subscribeGameTypes };
export const gameCategoriesStore: Readable<GameCategory[]> = {
	subscribe: subscribeGameCategories,
};
export const qnaCategoriesStore: Readable<QnACategory[]> = {
	subscribe: subscribeQnaCategories,
};

export function areStoresEmpty() {
	let isEmpty = true;

	const unsubGT = gameTypesStore.subscribe((gameTypes) => {
		isEmpty = isEmpty && gameTypes.length === 0;
	});
	unsubGT();

	const unsubGC = gameCategoriesStore.subscribe((gameCategories) => {
		isEmpty = isEmpty && gameCategories.length === 0;
	});
	unsubGC();

	const unsubQnAC = qnaCategoriesStore.subscribe((qnaCategories) => {
		isEmpty = isEmpty && qnaCategories.length === 0;
	});
	unsubQnAC();

	return isEmpty;
}

export function initStores(
	gameTypes: GameType[],
	gameCategories: GameCategory[],
	qnaCategories: QnACategory[],
) {
	console.debug("[stores] initStores called. areStoresEmpty=", areStoresEmpty());
	if (areStoresEmpty()) {
		console.debug(
			"[stores] setting gameTypes (%d), gameCategories (%d), qnaCategories (%d)",
			gameTypes.length,
			gameCategories.length,
			qnaCategories.length,
		);
		setGameTypes(gameTypes);
		setGameCategories(gameCategories);
		setQnaCategories(qnaCategories);
	}
	console.debug("[stores] initStores skipped because stores are not empty");
}

// Add small hooks to help debug accidental clears
export function _debug_getCurrentValues() {
	let values = {
		gameTypes: [] as GameType[],
		gameCategories: [] as GameCategory[],
		qnaCategories: [] as QnACategory[],
	};
	const u1 = gameTypesStore.subscribe((v) => (values.gameTypes = v));
	u1();
	const u2 = gameCategoriesStore.subscribe((v) => (values.gameCategories = v));
	u2();
	const u3 = qnaCategoriesStore.subscribe((v) => (values.qnaCategories = v));
	u3();
	return values;
}
