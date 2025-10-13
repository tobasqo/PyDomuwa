import { BaseApiRoute, type QueryParams } from "$lib/api/routes/BaseApiRoute";
import type {
	GameType,
	GameTypeCreate,
	GameTypeUpdate,
} from "$lib/api/types/game_type";
import type { AxiosInstance } from "axios";
import type { ApiResult } from "$lib/api/responses";
import type { QuestionWithAnswers } from "$lib/api/types/question";
import { makeApiRequest } from "$lib/api";

export class GameTypeApiRoute extends BaseApiRoute<
	GameTypeCreate,
	GameTypeUpdate,
	GameType
> {
	constructor() {
		super("/api/game-types/");
	}

	getAllQuestions = async (
		axiosInstance: AxiosInstance,
		modelId: number,
		params: QueryParams | undefined = undefined,
	): Promise<ApiResult<QuestionWithAnswers[]>> => {
		const urlParams = this.makeGetAllParams(params);
		return await makeApiRequest<QuestionWithAnswers[]>(axiosInstance, {
			method: "GET",
			url: this.routeUrl + modelId + "/questions",
			params: urlParams,
		});
	};
}
