package main

import (
	"context"
	b64 "encoding/base64"
	"flag"
	"fmt"
	"log"
	"math/rand"
	"net/http"
	"os"
	"os/signal"
	"time"

	lockedrand "github.com/fmeyer/upstream_server/lrand"
	"github.com/gorilla/mux"
)

const charset = "1234567890!@#$%^&*()abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
const charsetLen = len(charset)

// PingHandler handles ping with Pong
func PingHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, "ponGO\n")
}

// RandomHandler simulates a computing endpoint
func RandomHandler(w http.ResponseWriter, r *http.Request) {

	var rRand = lockedrand.LockedRand{Rand: rand.New(rand.NewSource(time.Now().UnixNano()))}

	n := rRand.ExpFloat64()
	time.Sleep(time.Duration(n) * time.Millisecond)

	w.WriteHeader(http.StatusOK)

	data := RandStringBytes(int(n * 1000))
	payload := b64.StdEncoding.EncodeToString([]byte(data))

	fmt.Fprintf(w, payload)
}

// RandStringBytes builds a random string of size n
func RandStringBytes(n int) string {
	var sRand = lockedrand.LockedRand{Rand: rand.New(rand.NewSource(time.Now().UnixNano()))}

	b := make([]byte, n)
	for i := range b {
		b[i] = charset[sRand.Intn(charsetLen)]
	}
	return string(b)
}

func main() {
	var wait time.Duration
	flag.DurationVar(&wait, "graceful-timeout", time.Second*15, "the duration for which the server gracefully wait for existing connections to finish - e.g. 15s or 1m")
	flag.Parse()

	r := mux.NewRouter()
	r.HandleFunc("/ping", PingHandler)
	r.HandleFunc("/random", RandomHandler)

	srv := &http.Server{
		Addr:         "0.0.0.0:8080",
		WriteTimeout: time.Second * 15,
		ReadTimeout:  time.Second * 15,
		IdleTimeout:  time.Second * 60,
		Handler:      r, // hook up handler
	}

	// Run server in a goroutine.
	go func() {
		if err := srv.ListenAndServe(); err != nil {
			log.Println(err)
		}
	}()

	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt)

	// Block until we receive our signal.
	<-c

	// Create a deadline to wait for.
	ctx, cancel := context.WithTimeout(context.Background(), wait)
	defer cancel()

	// Doesn't block if no connections, but will otherwise wait
	// until the timeout deadline.
	go func() {
		srv.Shutdown(ctx)
	}()

	<-ctx.Done()

	log.Println("shutting down")
	os.Exit(0)
}
