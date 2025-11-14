package main

import (
	"log"
	"os"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"

	pb "github.com/ManoVikram/AI-Podcast-Summarizer/backend/api/proto"
	"github.com/ManoVikram/AI-Podcast-Summarizer/backend/api/routes"
	"github.com/ManoVikram/AI-Podcast-Summarizer/backend/api/services"
	"github.com/gin-gonic/gin"
)

func main() {
	// Step 1 - Connect to the Python gRPC server
	grpcAddress := os.Getenv("GRPC_SERVER_ADDRESS")
	connection, err := grpc.NewClient(grpcAddress, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatal("Failed to connect to gRPC server: ", err)
		return
	}
	defer connection.Close()

	// Step 2 - Create a gRPC service client
	grpcClient := pb.NewPodcastSummarizerServiceClient(connection)

	// Step 3 - Initizialize services with the gRPC client
	services := &services.Services{
		AIclient: grpcClient,
	}

	// Step 3 - Initialize and set up the Gin server
	server := gin.Default()

	server.RedirectTrailingSlash = true

	// Step 4 - Register the routes to the Gin server and ingest the services for dependency injection
	routes.RegisterRoutes(server, services)

	// Step 5 - Start the Gin server
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	log.Fatal(server.Run(":" + port))
}
