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
  if (areStoresEmpty()) {
    setGameTypes(gameTypes);
    setGameCategories(gameCategories);
    setQnaCategories(qnaCategories);
  }
}
