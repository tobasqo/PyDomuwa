import { readCurrentUser } from "$lib/api/auth";
import { apiClient } from "$lib/api";

export const load = async ({ fetch, cookies }) => {
	await readCurrentUser(fetch, cookies);

	const [gameTypes, gameCategories, qnaCategories] = await Promise.all([
		apiClient.gameTypes.getAll(fetch, cookies),
		apiClient.gameCategories.getAll(fetch, cookies),
		apiClient.qnaCategories.getAll(fetch, cookies),
	]);

	return {
		gameRooms: [],
		initialData: {
			gameTypes,
			gameCategories,
			qnaCategories,
		},
	};
};
