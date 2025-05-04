package cache

import (
	"context"
	"log"
	"os"

	"github.com/redis/go-redis/v9"
)

var Ctx = context.Background()

func Connect() *redis.Client {
	url := os.Getenv("REDIS_URL")

	opt, err := redis.ParseURL(url)
	if err != nil {
		log.Fatalf("❌ Invalid Redis URL: %v", err)
	}

	rdb := redis.NewClient(opt)

	if err := rdb.Ping(Ctx).Err(); err != nil {
		log.Fatalf("❌ Redis connection failed: %v", err)
	}

	log.Println("✅ Redis connection established")
	return rdb
}
