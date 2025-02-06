import { z } from "zod";
import { PlayerSchema } from "$lib/api/types/player";

export const PlayerScoreSchema = z.object({
	id: z.number().min(1),
	player: PlayerSchema,
});
export type PlayerScore = z.infer<typeof PlayerScoreSchema>;

export const RankingSchema = z.object({
	id: z.string().min(1),
	gameRoomId: z.number().min(1),
	playerScores: z.array(PlayerScoreSchema),
});
export type Ranking = z.infer<typeof RankingSchema>;
