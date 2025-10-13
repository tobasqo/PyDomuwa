import { initStores } from "$lib/stores/global";

export const load = async ({ data }) => {
	initStores(data.gameTypes, data.gameCategories, data.qnaCategories);
	return {};
};
