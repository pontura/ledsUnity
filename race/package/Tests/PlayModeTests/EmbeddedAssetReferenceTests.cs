using NUnit.Framework;
using System;

using Rive.Tests.Utils;
using UnityEngine.TestTools;
using System.Collections;
using Rive.Utils;
namespace Rive.Tests
{
    public class EmbeddedAssetReferenceTests
    {
        private MockLogger mockLogger;

        [SetUp]
        public void Setup()
        {
            mockLogger = new MockLogger();
            DebugLogger.Instance = mockLogger;
        }

        [Test]
        public void Constructor_WithEmbeddedAssetData_SetsPropertiesCorrectly()
        {
            var embeddedAssetData = new EmbeddedAssetData(EmbeddedAssetType.Font, 1, "TestFont", 100);
            var reference = new FontEmbeddedAssetReference(embeddedAssetData, 0);

            Assert.AreEqual(EmbeddedAssetType.Font, reference.AssetType);
            Assert.AreEqual(1u, reference.Id);
            Assert.AreEqual("TestFont", reference.Name);
            Assert.AreEqual(100u, reference.EmbeddededBytesSize);
            Assert.AreEqual(0u, reference.IndexInRiveFile);
        }

        [Test]
        public void Constructor_WithIndividualParameters_SetsPropertiesCorrectly()
        {
            var outOfBandAsset = OutOfBandAsset.Create<FontOutOfBandAsset>(new byte[100]);
            var reference = new FontEmbeddedAssetReference(EmbeddedAssetType.Font, 1, "TestFont", 100, 0, outOfBandAsset);

            Assert.AreEqual(EmbeddedAssetType.Font, reference.AssetType);
            Assert.AreEqual(1u, reference.Id);
            Assert.AreEqual("TestFont", reference.Name);
            Assert.AreEqual(100u, reference.EmbeddededBytesSize);
            Assert.AreEqual(0u, reference.IndexInRiveFile);
            Assert.AreEqual(outOfBandAsset, reference.OutOfBandAssetToLoad);
        }

        [Test]
        public void SetRiveFileReference_SetsWeakReference()
        {
            var reference = new FontEmbeddedAssetReference(EmbeddedAssetType.Font, 1, "TestFont", 100, 0, null);

            var file = new Rive.File(IntPtr.Zero, 0, null);
            Assert.IsFalse(reference.HasFileReference());

            reference.SetRiveFileReference(file);

            Assert.IsTrue(reference.HasFileReference());
            Assert.IsFalse(mockLogger.AnyLogTypeContains(EmbeddedAssetReference.WarningCodes.FILE_NOT_LOADED));
        }

        [Test]
        public void UpdateEmbeddedAssetReferenceInFile_WithNullAsset_LogsWarning()
        {
            var reference = new FontEmbeddedAssetReference(EmbeddedAssetType.Font, 1, "TestFont", 100, 0, null);

            reference.SetFont(null);


            Assert.IsTrue(mockLogger.AnyLogTypeContains(EmbeddedAssetReference.WarningCodes.NULL_OOB_ASSET));

        }

        [Test]
        public void UpdateEmbeddedAssetReferenceInFile_WithoutFileReference_LogsWarning()
        {
            var reference = new FontEmbeddedAssetReference(EmbeddedAssetType.Font, 1, "TestFont", 100, 0, null);
            var fontAsset = OutOfBandAsset.Create<FontOutOfBandAsset>(new byte[100]);

            reference.SetFont(fontAsset);

            Assert.IsTrue(mockLogger.AnyLogTypeContains(EmbeddedAssetReference.WarningCodes.FILE_NOT_LOADED));

        }

        [Test]
        public void UpdateEmbeddedAssetReferenceInFile_WithFileReference_UpdatesFile()
        {
            var mockFile = new Rive.File(IntPtr.Zero, 0, null);
            var reference = new FontEmbeddedAssetReference(EmbeddedAssetType.Font, 1, "TestFont", 100, 0, null);
            var fontAsset = OutOfBandAsset.Create<FontOutOfBandAsset>(new byte[100]);

            reference.SetRiveFileReference(mockFile);
            reference.SetFont(fontAsset);

            Assert.False(mockLogger.AnyLogTypeContains(EmbeddedAssetReference.WarningCodes.FILE_NOT_LOADED));

        }

        [UnityTest]
        public IEnumerator UpdateEmbeddedAssetReferenceInFile_WithReleasedFileReference_LogsWarning()
        {
            var reference = new FontEmbeddedAssetReference(EmbeddedAssetType.Font, 1, "TestFont", 100, 0, null);

            var file = new Rive.File(IntPtr.Zero, 0, null);
            var fontAsset = OutOfBandAsset.Create<FontOutOfBandAsset>(new byte[100]);

            fontAsset.Load();
            reference.SetRiveFileReference(file);

            Assert.IsTrue(reference.HasFileReference());

            // Try to force garbage collection multiple times to release the weak reference
            file = null;
            for (int i = 0; i < 5; i++)
            {
                GC.Collect(GC.MaxGeneration, GCCollectionMode.Forced, true);
                GC.WaitForPendingFinalizers();
                yield return null;
            }


            reference.SetFont(fontAsset);

            Assert.IsFalse(reference.HasFileReference());
            Assert.IsTrue(mockLogger.AnyLogTypeContains(EmbeddedAssetReference.WarningCodes.FILE_RELEASED));
            fontAsset.Unload();
        }
    }
}