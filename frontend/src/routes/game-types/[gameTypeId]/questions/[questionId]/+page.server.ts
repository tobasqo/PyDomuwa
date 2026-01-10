import { apiClient } from "$lib/api/client";
import { type Actions, error, redirect } from "@sveltejs/kit";

export const load = async ({ fetch, params, cookies }) => {
  const gameTypeId = parseInt(params.gameTypeId);
  const [gameType, questions] = await Promise.all([
    apiClient.getGameType(fetch, cookies, gameTypeId),
    apiClient.getAllQuestionsForGameType(fetch, cookies, gameTypeId),
  ]);
  return { gameType, questions };
};

export const actions = {
  toggleExclude: async ({ fetch, cookies, request, params }) => {
    if (params.gameTypeId === undefined) {
      throw error(400, "`gameTypeId` not found in path");
    }
    const gameTypeId = parseInt(params.gameTypeId);
    if (params.questionId === undefined) {
      throw error(400, "`questionId` not found in path");
    }
    const questionId = parseInt(params.questionId);
    const formData = await request.formData();
    const exclude = formData.get("exclude");
    if (exclude === null) {
      throw error(400, "`exclude` not found in form");
    }
    console.debug(`toggling exclude for question=${questionId} exclude=${exclude}`);
    await apiClient.updateQuestion(fetch, cookies, questionId, {
      excluded: exclude === "true",
    });
    throw redirect(303, `/game-types/${gameTypeId}/questions`)
  },
} satisfies Actions;
