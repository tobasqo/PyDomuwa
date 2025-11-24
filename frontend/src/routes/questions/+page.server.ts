import {type Actions, isActionFailure, redirect} from "@sveltejs/kit";
import {apiClient} from "$lib/api/client";

export const load = async ({ fetch, cookies, url }) => {
  const gameTypeId = parseInt(url.searchParams.get("gameTypeId")!);
  const [gameType, qnaCategories] = await Promise.all([
    apiClient.getGameType(fetch, cookies, gameTypeId),
    apiClient.getAllQnACategories(fetch, cookies),
  ]);
  return { gameType, qnaCategories };
}

export const actions = {
  default: async({fetch, cookies, request, url}) => {
    const formData = await request.formData();
    const gameTypeId = parseInt(url.searchParams.get("gameTypeId")!);
    const questionData = {
      text: formData.get("text")!.toString(),
      gameTypeId: gameTypeId,
      gameCategoryId: parseInt(formData.get("game-category")!.toString()),
    };
    const result = await apiClient.createQuestion(fetch, cookies, questionData);
    if (isActionFailure(result)) {
      return result;
    }
    throw redirect(303, `/game-types/${gameTypeId}`);
  }
} satisfies Actions;
