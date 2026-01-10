import { apiClient } from "$lib/api/client";
import { type Question } from "$lib/api/types/question";
import { type Actions, error, isActionFailure, redirect } from "@sveltejs/kit";

export const load = async ({ fetch, cookies, params }) => {
  const gameTypeId = parseInt(params.gameTypeId);
  const questionId = parseInt(params.questionId);
  const [gameType, qnaCategories, question] = await Promise.all([
    apiClient.getGameType(fetch, cookies, gameTypeId),
    apiClient.getAllQnACategories(fetch, cookies),
    apiClient.getQuestion(fetch, cookies, questionId),
  ]);
  return { gameType, qnaCategories, question };
};

export const actions = {
  edit: async ({ fetch, cookies, request, params }) => {
    if (params.gameTypeId === undefined) {
      throw error(400, "`gameTypeId` not found in path");
    }
    const gameTypeId = parseInt(params.gameTypeId);
    if (params.questionId === undefined) {
      throw error(400, "`questionId` not found in path");
    }
    const questionId = parseInt(params.questionId);
    const formData = await request.formData();
    const questionUpdateData = {
      text: formData.get("text") as string,
      gameCategoryId: parseInt(formData.get("game-category") as string),
    };
    const result = await apiClient.updateQuestion(
      fetch,
      cookies,
      questionId,
      questionUpdateData,
    );
    if (isActionFailure(result)) {
      return result;
    }
    throw redirect(
      303,
      `/game-types/${gameTypeId}/questions/${(result as Question).id}`,
    );
  },
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
    throw redirect(303, `/game-types/${gameTypeId}/questions`);
  },
} satisfies Actions;
