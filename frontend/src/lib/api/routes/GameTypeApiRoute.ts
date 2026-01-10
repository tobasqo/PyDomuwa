import { BaseApiRoute, type QueryParams } from "$lib/api/routes/BaseApiRoute";
import type { GameTypeCreate, GameTypeUpdate } from "$lib/api/types/game_type";
import { makeApiRequest, type Fetch } from "$lib/api";
import type { Cookies } from "@sveltejs/kit";

export class GameTypeApiRoute extends BaseApiRoute<GameTypeCreate, GameTypeUpdate> {
  constructor() {
    super("/api/game-types/");
  }

  getAllQuestions = async (
    fetch: Fetch,
    cookies: Cookies,
    modelId: number,
    params: QueryParams | undefined = undefined,
  ) => {
    const urlParams = this.makeGetAllParams(params);
    const url = this.routeUrl + modelId + "/questions" + "?" + urlParams.toString();
    return await makeApiRequest(fetch, cookies, url, {
      method: "GET",
    });
  };
}
