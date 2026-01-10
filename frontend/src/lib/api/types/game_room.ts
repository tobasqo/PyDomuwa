import { z } from "zod";
import { GameTypeSchema } from "$lib/api/types/game_type";
import { GameCategorySchema } from "$lib/api/types/game_category";
import { QuestionWithAnswersSchema } from "$lib/api/types/question";
import { RankingSchema } from "$lib/api/types/ranking";
import { PlayerSchema } from "$lib/api/types/player";

export const GameRoomSchema = z.object({
  id: z.number().min(0),
  websocket: z.string(),
  createdAt: z.date(),
  rounds: z.number().min(1),
  curRound: z.number().min(1),
  gameType: GameTypeSchema,
  gameCategory: GameCategorySchema,
  questions: z.array(QuestionWithAnswersSchema),
  players: z.array(PlayerSchema),
  ranking: RankingSchema,
});
