//! Windows-only, RAM-only evidence contract for a *future* R4 xShm handle-bound VFS.
//! This tests a design boundary, not native Windows handles or SQLite.
//! Real R3 has no xShm* support; test-only D3a delegates xShm* to stock Win32.
//! A matching file name, even with FileId128, never authenticates the handle
//! that stock xShmMap actually mapped. No runtime admission can be minted here.

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
struct Identity {
    volume: u64,
    file_id_128: [u8; 16],
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum Provenance {
    HeldNativeHandle,
    ActualXShmMapNativeHandle,
    ReopenedNameOnly,
    DelegatedWithoutHandleBinding,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
struct Evidence {
    identity: Identity,
    provenance: Provenance,
    epoch: u64,
    live: bool,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
struct EvidenceBundle {
    main: Option<Evidence>,
    wal: Option<Evidence>,
    shm: Option<Evidence>,
    mapped_shm: Option<Evidence>,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum DesignDecision {
    RefuseUnboundOrStale,
    TemplateCompleteButRuntimeStillForbidden,
}

// No return type can admit production, open SQLite or build V7WriterAdmission.
// Positive results only express *requirements on a future native prototype*.
fn evaluate_design_evidence(bundle: EvidenceBundle) -> DesignDecision {
    let (Some(main), Some(wal), Some(shm), Some(mapped)) =
        (bundle.main, bundle.wal, bundle.shm, bundle.mapped_shm)
    else { return DesignDecision::RefuseUnboundOrStale };
    if main.epoch == 0
        || [wal, shm, mapped].iter().any(|e| e.epoch != main.epoch)
        || [main, wal, shm, mapped].iter().any(|e| !e.live)
        || main.provenance != Provenance::HeldNativeHandle
        || wal.provenance != Provenance::HeldNativeHandle
        || shm.provenance != Provenance::HeldNativeHandle
        || mapped.provenance != Provenance::ActualXShmMapNativeHandle
        || mapped.identity != shm.identity
        || main.identity == wal.identity
        || main.identity == shm.identity
        || wal.identity == shm.identity
    {
        return DesignDecision::RefuseUnboundOrStale;
    }
    DesignDecision::TemplateCompleteButRuntimeStillForbidden
}

#[cfg(test)]
mod tests {
    use super::*;

    fn id(n: u8) -> Identity { Identity { volume: 42, file_id_128: [n; 16] } }
    fn held(n: u8) -> Evidence {
        Evidence { identity: id(n), provenance: Provenance::HeldNativeHandle, epoch: 11, live: true }
    }
    fn bundle() -> EvidenceBundle {
        EvidenceBundle {
            main: Some(held(1)),
            wal: Some(held(2)),
            shm: Some(held(3)),
            mapped_shm: Some(Evidence {
                provenance: Provenance::ActualXShmMapNativeHandle, ..held(3)
            }),
        }
    }
    fn refused(b: EvidenceBundle) {
        assert_eq!(evaluate_design_evidence(b), DesignDecision::RefuseUnboundOrStale);
    }

    #[test]
    fn r4_model_complete_evidence_still_not_runtime_writer_admission() {
        assert_eq!(evaluate_design_evidence(bundle()),
            DesignDecision::TemplateCompleteButRuntimeStillForbidden);
    }

    #[test]
    fn r4_model_rejects_name_only_shm_even_with_matching_fileid128() {
        let mut b = bundle();
        b.shm.as_mut().unwrap().provenance = Provenance::ReopenedNameOnly;
        refused(b);
    }

    #[test]
    fn r4_model_rejects_stock_delegation_without_real_xshm_handle_binding() {
        let mut b = bundle();
        b.mapped_shm.as_mut().unwrap().provenance = Provenance::DelegatedWithoutHandleBinding;
        refused(b);
    }

    #[test]
    fn r4_model_rejects_different_xshm_mapped_file_identity() {
        let mut b = bundle();
        b.mapped_shm.as_mut().unwrap().identity = id(4);
        refused(b);
    }

    #[test]
    fn r4_model_rejects_cross_epoch_fileid_matching_aba() {
        let mut b = bundle();
        b.mapped_shm.as_mut().unwrap().epoch = 12;
        refused(b);
    }

    #[test]
    fn r4_model_rejects_closed_mapped_shm_handle_and_revokes() {
        let mut b = bundle();
        assert_eq!(evaluate_design_evidence(b),
            DesignDecision::TemplateCompleteButRuntimeStillForbidden);
        b.mapped_shm.as_mut().unwrap().live = false;
        refused(b);
    }

    #[test]
    fn r4_model_rejects_missing_wal_or_shm_handle() {
        let mut b = bundle();
        b.wal = None;
        refused(b);
        let mut b = bundle();
        b.shm = None;
        refused(b);
    }

    #[test]
    fn r4_model_rejects_main_wal_or_shm_aliasing_same_fileid() {
        let mut b = bundle();
        b.wal.as_mut().unwrap().identity = id(1);
        refused(b);
        let mut b = bundle();
        b.shm.as_mut().unwrap().identity = id(2);
        b.mapped_shm.as_mut().unwrap().identity = id(2);
        refused(b);
    }

    #[test]
    fn r4_model_rejects_unpinned_main_even_when_fileid_matches() {
        let mut b = bundle();
        b.main.as_mut().unwrap().provenance = Provenance::ReopenedNameOnly;
        refused(b);
    }

    #[test]
    fn r4_model_rejects_zero_epoch_or_stale_sidecar() {
        let mut b = bundle();
        b.main.as_mut().unwrap().epoch = 0;
        refused(b);
        let mut b = bundle();
        b.shm.as_mut().unwrap().epoch = 99;
        refused(b);
    }
}
