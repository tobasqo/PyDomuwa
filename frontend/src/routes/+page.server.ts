import { readCurrentUser } from "$lib/api/auth";
import { apiClient } from "$lib/api";
import { initStores, areStoresEmpty } from "$lib/stores/global";

export const load = async ({ fetch, cookies }) => {
	await readCurrentUser(fetch, cookies);

	// Only fetch and initialize stores if they're empty
	if (areStoresEmpty()) {
		// Parallelize the requests
		const [gameTypes, gameCategories, qnaCategories] = await Promise.all([
			apiClient.gameTypes.getAll(fetch, cookies),
			apiClient.gameCategories.getAll(fetch, cookies),
			apiClient.qnaCategories.getAll(fetch, cookies)
		]);
		
		initStores(gameTypes, gameCategories, qnaCategories);
	}
	
	return { gameRooms: [] };
};
