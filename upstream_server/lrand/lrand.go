package lockedrand

import (
	"math/rand"
	"sync"
)

// LockedRand concurrent rand
type LockedRand struct {
	lk sync.Mutex
	*rand.Rand
}

// Seed the concurrent rand
func (r *LockedRand) Seed(seed int64) {
	r.lk.Lock()
	r.Rand.Seed(seed)
	r.lk.Unlock()
}

// Read implements the read interface
func (r *LockedRand) Read(p []byte) (n int, err error) {
	r.lk.Lock()
	n, err = r.Rand.Read(p)
	r.lk.Unlock()
	return n, err
}
